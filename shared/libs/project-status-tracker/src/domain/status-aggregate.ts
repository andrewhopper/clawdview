// File UUID: 7e62230f-d62e-4ac1-b573-e963516e8cf4
// File UUID: i6j7k8l9-3m4n-5o1p-9q5r-8s9t1u2v3w4x

import type {
  StatusEvent,
  Todo,
  Comment,
  ProjectCounts,
  TodoStatus,
  Priority,
  ListTodosOptions,
} from './types.js';

/**
 * Status aggregate - rebuilds current state from events
 */
export class StatusAggregate {
  private todos: Map<string, Todo> = new Map();
  private comments: Map<string, Comment> = new Map();
  private projectCounts: Map<string, ProjectCounts> = new Map();

  /**
   * Replay events to rebuild state
   */
  replay(events: StatusEvent[]): void {
    this.todos.clear();
    this.comments.clear();
    this.projectCounts.clear();

    for (const event of events) {
      this.applyEvent(event);
    }
  }

  /**
   * Apply a single event to update state
   */
  applyEvent(event: StatusEvent): void {
    switch (event.type) {
      case 'TODO_CREATED':
        this.handleTodoCreated(event);
        break;
      case 'TODO_COMPLETED':
        this.handleTodoCompleted(event);
        break;
      case 'TODO_UNCOMPLETED':
        this.handleTodoUncompleted(event);
        break;
      case 'TODO_UPDATED':
        this.handleTodoUpdated(event);
        break;
      case 'TODO_DELETED':
        this.handleTodoDeleted(event);
        break;
      case 'COMMENT_ADDED':
        this.handleCommentAdded(event);
        break;
      case 'STATUS_UPDATED':
        this.handleStatusUpdated(event);
        break;
    }
  }

  private handleTodoCreated(event: StatusEvent): void {
    const { todoId, title, description, priority, assignee } = event.payload as {
      todoId: string;
      title: string;
      description?: string;
      priority?: Priority;
      assignee?: string;
    };

    const todo: Todo = {
      id: todoId,
      shortId: this.generateShortId(todoId),
      projectId: event.projectId,
      title,
      description,
      status: 'active' as TodoStatus,
      priority: priority || ('medium' as Priority),
      assignee,
      tags: [],
      createdAt: event.timestamp,
      updatedAt: event.timestamp,
    };

    this.todos.set(todoId, todo);
    this.incrementProjectCount(event.projectId, 'active');
  }

  private handleTodoCompleted(event: StatusEvent): void {
    const todo = this.todos.get(event.entityId);
    if (!todo) return;

    const oldStatus = todo.status;
    todo.status = 'completed' as TodoStatus;
    todo.completedAt = event.timestamp;
    todo.updatedAt = event.timestamp;

    this.decrementProjectCount(event.projectId, oldStatus);
    this.incrementProjectCount(event.projectId, 'completed');
  }

  private handleTodoUncompleted(event: StatusEvent): void {
    const todo = this.todos.get(event.entityId);
    if (!todo) return;

    const oldStatus = todo.status;
    todo.status = 'active' as TodoStatus;
    todo.completedAt = undefined;
    todo.updatedAt = event.timestamp;

    this.decrementProjectCount(event.projectId, oldStatus);
    this.incrementProjectCount(event.projectId, 'active');
  }

  private handleTodoUpdated(event: StatusEvent): void {
    const todo = this.todos.get(event.entityId);
    if (!todo) return;

    const { title, description, priority, assignee, tags } = event.payload as {
      title?: string;
      description?: string;
      priority?: Priority;
      assignee?: string;
      tags?: string[];
    };

    if (title !== undefined) todo.title = title;
    if (description !== undefined) todo.description = description;
    if (priority !== undefined) todo.priority = priority;
    if (assignee !== undefined) todo.assignee = assignee;
    if (tags !== undefined) todo.tags = tags;

    todo.updatedAt = event.timestamp;
  }

  private handleTodoDeleted(event: StatusEvent): void {
    const todo = this.todos.get(event.entityId);
    if (!todo) return;

    const oldStatus = todo.status;
    todo.status = 'deleted' as TodoStatus;
    todo.deletedAt = event.timestamp;
    todo.updatedAt = event.timestamp;

    this.decrementProjectCount(event.projectId, oldStatus);
    this.incrementProjectCount(event.projectId, 'deleted');
  }

  private handleCommentAdded(event: StatusEvent): void {
    const { commentId, content, author } = event.payload as {
      commentId: string;
      content: string;
      author: string;
    };

    const comment: Comment = {
      id: commentId,
      projectId: event.projectId,
      content,
      author,
      createdAt: event.timestamp,
    };

    this.comments.set(commentId, comment);
  }

  private handleStatusUpdated(event: StatusEvent): void {
    // Generic status update (can be deprecated in favor of specific events)
    const todo = this.todos.get(event.entityId);
    if (!todo) return;

    const { status } = event.payload as { status: TodoStatus };
    const oldStatus = todo.status;

    todo.status = status;
    todo.updatedAt = event.timestamp;

    if (status === 'completed') {
      todo.completedAt = event.timestamp;
    }

    this.decrementProjectCount(event.projectId, oldStatus);
    this.incrementProjectCount(event.projectId, status);
  }

  private incrementProjectCount(projectId: string, status: TodoStatus): void {
    const counts = this.getOrCreateProjectCounts(projectId);

    if (status === 'active') counts.active++;
    else if (status === 'completed') counts.completed++;
    else if (status === 'blocked') counts.blocked++;

    counts.total++;
  }

  private decrementProjectCount(projectId: string, status: TodoStatus): void {
    const counts = this.getOrCreateProjectCounts(projectId);

    if (status === 'active') counts.active = Math.max(0, counts.active - 1);
    else if (status === 'completed') counts.completed = Math.max(0, counts.completed - 1);
    else if (status === 'blocked') counts.blocked = Math.max(0, counts.blocked - 1);

    counts.total = Math.max(0, counts.total - 1);
  }

  private getOrCreateProjectCounts(projectId: string): ProjectCounts {
    let counts = this.projectCounts.get(projectId);
    if (!counts) {
      counts = {
        projectId,
        active: 0,
        completed: 0,
        blocked: 0,
        total: 0,
      };
      this.projectCounts.set(projectId, counts);
    }
    return counts;
  }

  private generateShortId(id: string): string {
    // Take first 8 chars of ULID/UUID
    return id.substring(0, 8).toUpperCase();
  }

  /**
   * Query todos with filters
   */
  listTodos(options: ListTodosOptions = {}): Todo[] {
    let results = Array.from(this.todos.values());

    // Filter by project
    if (options.projectId) {
      results = results.filter((t) => t.projectId === options.projectId);
    }

    // Filter by status
    if (options.status) {
      results = results.filter((t) => t.status === options.status);
    }

    // Filter by priority
    if (options.priority) {
      results = results.filter((t) => t.priority === options.priority);
    }

    // Filter by assignee
    if (options.assignee) {
      results = results.filter((t) => t.assignee === options.assignee);
    }

    // Filter by tags
    if (options.tags && options.tags.length > 0) {
      results = results.filter((t) =>
        options.tags!.some((tag) => t.tags?.includes(tag))
      );
    }

    // Apply pagination
    if (options.offset) {
      results = results.slice(options.offset);
    }

    if (options.limit) {
      results = results.slice(0, options.limit);
    }

    return results;
  }

  /**
   * Get todo counts for a project
   */
  getTodoCounts(projectId: string): ProjectCounts {
    return (
      this.projectCounts.get(projectId) || {
        projectId,
        active: 0,
        completed: 0,
        blocked: 0,
        total: 0,
      }
    );
  }

  /**
   * Get a single todo by ID or shortId
   */
  getTodo(id: string): Todo | undefined {
    // Try exact match first
    if (this.todos.has(id)) {
      return this.todos.get(id);
    }

    // Try shortId match
    const shortId = id.toUpperCase();
    return Array.from(this.todos.values()).find((t) => t.shortId === shortId);
  }

  /**
   * Get comments for a project
   */
  getComments(projectId: string, limit?: number): Comment[] {
    let results = Array.from(this.comments.values()).filter(
      (c) => c.projectId === projectId
    );

    if (limit) {
      results = results.slice(0, limit);
    }

    return results;
  }
}
