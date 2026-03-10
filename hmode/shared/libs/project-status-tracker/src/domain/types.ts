// File UUID: c2b34171-abfe-4c1f-97a4-a92c2e7fe7c7
// File UUID: o3p4q5r6-9s1t-9u7v-9w2x-5y6z7a8b9c1d

/**
 * Event types for status tracking (simplified for MVP)
 */
export type StatusEventType =
  | 'TODO_CREATED'
  | 'TODO_COMPLETED'
  | 'TODO_UNCOMPLETED'
  | 'TODO_UPDATED'
  | 'TODO_DELETED'
  | 'COMMENT_ADDED'
  | 'STATUS_UPDATED';

/**
 * Todo priority levels
 */
export type Priority = 'low' | 'medium' | 'high' | 'critical';

/**
 * Todo status states
 */
export type TodoStatus = 'active' | 'completed' | 'blocked' | 'deleted';

/**
 * Domain event structure (simplified)
 */
export interface StatusEvent {
  id: string; // ULID
  timestamp: string; // ISO 8601
  type: StatusEventType;
  projectId: string; // Project UUID
  entityId: string; // Todo/comment ULID
  payload: Record<string, unknown>;
  createdAt?: string; // Database timestamp
}

/**
 * Todo entity (materialized from events)
 */
export interface Todo {
  id: string; // ULID
  shortId: string; // First 8 chars of ULID for human-friendly reference
  projectId: string;
  title: string;
  description?: string;
  status: TodoStatus;
  priority: Priority;
  assignee?: string;
  tags?: string[];
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  deletedAt?: string;
}

/**
 * Comment entity (materialized from events)
 */
export interface Comment {
  id: string; // ULID
  projectId: string;
  content: string;
  author: string;
  createdAt: string;
}

/**
 * Project status counts
 */
export interface ProjectCounts {
  projectId: string;
  active: number;
  completed: number;
  blocked: number;
  total: number;
}

/**
 * Query options for listing todos
 */
export interface ListTodosOptions {
  projectId?: string;
  status?: TodoStatus;
  priority?: Priority;
  assignee?: string;
  tags?: string[];
  limit?: number;
  offset?: number;
}

/**
 * Options for creating a todo
 */
export interface CreateTodoOptions {
  description?: string;
  priority?: Priority;
  assignee?: string;
  tags?: string[];
}

/**
 * Options for updating a todo
 */
export interface UpdateTodoOptions {
  title?: string;
  description?: string;
  priority?: Priority;
  assignee?: string;
  tags?: string[];
}
