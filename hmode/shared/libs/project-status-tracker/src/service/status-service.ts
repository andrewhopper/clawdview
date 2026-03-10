// File UUID: 5624858e-f2d3-4d75-9f3d-9e970e23fef8
// File UUID: j7k8l9m1-4n5o-6p2q-9r6s-9t1u2v3w4x5y

import { EventStore } from '../db/event-store.js';
import { StatusAggregate } from '../domain/status-aggregate.js';
import type {
  Todo,
  Comment,
  ProjectCounts,
  CreateTodoOptions,
  UpdateTodoOptions,
  ListTodosOptions,
} from '../domain/types.js';
import { ulid } from 'ulid';

/**
 * High-level service for status tracking
 * Pattern: Write → Refresh → Read
 */
export class StatusService {
  private eventStore: EventStore;
  private aggregate: StatusAggregate;

  constructor(dbPath?: string) {
    this.eventStore = new EventStore(dbPath);
    this.aggregate = new StatusAggregate();
    this.refresh();
  }

  /**
   * Refresh aggregate state from event store
   */
  private refresh(projectId?: string): void {
    const events = this.eventStore.getEvents(projectId);
    this.aggregate.replay(events);
  }

  /**
   * Add a new todo
   */
  addTodo(
    projectId: string,
    title: string,
    options: CreateTodoOptions = {}
  ): Todo {
    const todoId = ulid();

    this.eventStore.append('TODO_CREATED', projectId, todoId, {
      todoId,
      title,
      description: options.description,
      priority: options.priority || 'medium',
      assignee: options.assignee,
      tags: options.tags || [],
    });

    this.refresh(projectId);

    const todo = this.aggregate.getTodo(todoId);
    if (!todo) {
      throw new Error('Failed to create todo');
    }

    return todo;
  }

  /**
   * Complete a todo
   */
  completeTodo(shortIdOrId: string): Todo {
    const todo = this.aggregate.getTodo(shortIdOrId);
    if (!todo) {
      throw new Error(`Todo not found: ${shortIdOrId}`);
    }

    this.eventStore.append('TODO_COMPLETED', todo.projectId, todo.id, {
      todoId: todo.id,
      completedAt: new Date().toISOString(),
    });

    this.refresh(todo.projectId);

    const updated = this.aggregate.getTodo(todo.id);
    if (!updated) {
      throw new Error('Failed to complete todo');
    }

    return updated;
  }

  /**
   * Uncomplete a todo (reopen)
   */
  uncompleteTodo(shortIdOrId: string): Todo {
    const todo = this.aggregate.getTodo(shortIdOrId);
    if (!todo) {
      throw new Error(`Todo not found: ${shortIdOrId}`);
    }

    this.eventStore.append('TODO_UNCOMPLETED', todo.projectId, todo.id, {
      todoId: todo.id,
    });

    this.refresh(todo.projectId);

    const updated = this.aggregate.getTodo(todo.id);
    if (!updated) {
      throw new Error('Failed to uncomplete todo');
    }

    return updated;
  }

  /**
   * Update todo details
   */
  updateTodo(shortIdOrId: string, options: UpdateTodoOptions): Todo {
    const todo = this.aggregate.getTodo(shortIdOrId);
    if (!todo) {
      throw new Error(`Todo not found: ${shortIdOrId}`);
    }

    this.eventStore.append('TODO_UPDATED', todo.projectId, todo.id, {
      todoId: todo.id,
      ...options,
    });

    this.refresh(todo.projectId);

    const updated = this.aggregate.getTodo(todo.id);
    if (!updated) {
      throw new Error('Failed to update todo');
    }

    return updated;
  }

  /**
   * Delete a todo (soft delete)
   */
  deleteTodo(shortIdOrId: string): void {
    const todo = this.aggregate.getTodo(shortIdOrId);
    if (!todo) {
      throw new Error(`Todo not found: ${shortIdOrId}`);
    }

    this.eventStore.append('TODO_DELETED', todo.projectId, todo.id, {
      todoId: todo.id,
      deletedAt: new Date().toISOString(),
    });

    this.refresh(todo.projectId);
  }

  /**
   * Add a comment
   */
  addComment(
    projectId: string,
    content: string,
    author: string
  ): Comment {
    const commentId = ulid();

    this.eventStore.append('COMMENT_ADDED', projectId, commentId, {
      commentId,
      content,
      author,
    });

    this.refresh(projectId);

    return {
      id: commentId,
      projectId,
      content,
      author,
      createdAt: new Date().toISOString(),
    };
  }

  /**
   * List todos with filters
   */
  listTodos(options: ListTodosOptions = {}): Todo[] {
    // Refresh if querying specific project
    if (options.projectId) {
      this.refresh(options.projectId);
    }

    return this.aggregate.listTodos(options);
  }

  /**
   * Get todo counts for a project
   */
  getProjectCounts(projectId: string): ProjectCounts {
    this.refresh(projectId);
    return this.aggregate.getTodoCounts(projectId);
  }

  /**
   * Get a single todo
   */
  getTodo(shortIdOrId: string): Todo | undefined {
    return this.aggregate.getTodo(shortIdOrId);
  }

  /**
   * Get comments for a project
   */
  getComments(projectId: string, limit?: number): Comment[] {
    this.refresh(projectId);
    return this.aggregate.getComments(projectId, limit);
  }

  /**
   * Get recent activity across all projects
   */
  getRecentActivity(limit = 50) {
    return this.eventStore.getRecentEvents(undefined, limit);
  }

  /**
   * Close the service and database connection
   */
  close(): void {
    this.eventStore.close();
  }
}
