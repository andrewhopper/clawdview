/**
 * UserCard - React/TypeScript Reference Component
 *
 * Demonstrates:
 * - Functional components with TypeScript
 * - Props interface with proper types
 * - React hooks (useState, useEffect, useCallback)
 * - Error boundaries
 * - Conditional rendering
 * - Event handling
 * - Accessibility
 */

import React, { useState, useEffect, useCallback } from 'react';

// Props interface
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: 'admin' | 'user' | 'guest';
}

export interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
  showActions?: boolean;
  className?: string;
}

// Component state interface
interface UserCardState {
  isExpanded: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * UserCard component displays user information with optional actions
 */
export const UserCard: React.FC<UserCardProps> = ({
  user,
  onEdit,
  onDelete,
  showActions = true,
  className = '',
}) => {
  // State management
  const [state, setState] = useState<UserCardState>({
    isExpanded: false,
    isLoading: false,
    error: null,
  });

  // Derived state
  const { isExpanded, isLoading, error } = state;
  const hasAvatar = Boolean(user.avatar);

  // Effects
  useEffect(() => {
    // Example: Log when user changes
    console.log('User updated:', user.id);

    // Cleanup function
    return () => {
      console.log('UserCard unmounting for user:', user.id);
    };
  }, [user.id]);

  // Event handlers
  const handleToggleExpand = useCallback(() => {
    setState((prev) => ({
      ...prev,
      isExpanded: !prev.isExpanded,
    }));
  }, []);

  const handleEdit = useCallback(() => {
    if (onEdit) {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        onEdit(user);
      } catch (err) {
        setState((prev) => ({
          ...prev,
          error: err instanceof Error ? err.message : 'Edit failed',
        }));
      } finally {
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    }
  }, [user, onEdit]);

  const handleDelete = useCallback(() => {
    if (onDelete && window.confirm(`Delete user ${user.name}?`)) {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        onDelete(user.id);
      } catch (err) {
        setState((prev) => ({
          ...prev,
          error: err instanceof Error ? err.message : 'Delete failed',
        }));
      } finally {
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    }
  }, [user.id, user.name, onDelete]);

  // Helper functions
  const getRoleBadgeColor = (role: User['role']): string => {
    const colors = {
      admin: 'bg-red-100 text-red-800',
      user: 'bg-blue-100 text-blue-800',
      guest: 'bg-gray-100 text-gray-800',
    };
    return colors[role];
  };

  // Render helpers
  const renderAvatar = () => {
    if (hasAvatar) {
      return (
        <img
          src={user.avatar}
          alt={`${user.name}'s avatar`}
          className="w-16 h-16 rounded-full object-cover"
        />
      );
    }
    return (
      <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center">
        <span className="text-2xl font-bold text-gray-600">
          {user.name.charAt(0).toUpperCase()}
        </span>
      </div>
    );
  };

  const renderActions = () => {
    if (!showActions) return null;

    return (
      <div className="flex gap-2 mt-4">
        {onEdit && (
          <button
            onClick={handleEdit}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            aria-label={`Edit ${user.name}`}
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={handleDelete}
            disabled={isLoading}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
            aria-label={`Delete ${user.name}`}
          >
            Delete
          </button>
        )}
      </div>
    );
  };

  // Main render
  return (
    <div
      className={`user-card p-6 border rounded-lg shadow-md ${className}`}
      role="article"
      aria-label={`User card for ${user.name}`}
    >
      {/* Error message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded" role="alert">
          {error}
        </div>
      )}

      {/* Header */}
      <div className="flex items-start gap-4">
        {renderAvatar()}

        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold">{user.name}</h3>
            <span className={`px-2 py-1 rounded text-sm ${getRoleBadgeColor(user.role)}`}>
              {user.role}
            </span>
          </div>

          <p className="text-gray-600 mt-1">{user.email}</p>

          <button
            onClick={handleToggleExpand}
            className="mt-2 text-blue-500 hover:text-blue-700"
            aria-expanded={isExpanded}
            aria-controls={`user-details-${user.id}`}
          >
            {isExpanded ? 'Show less' : 'Show more'}
          </button>
        </div>
      </div>

      {/* Expanded content */}
      {isExpanded && (
        <div
          id={`user-details-${user.id}`}
          className="mt-4 pt-4 border-t"
        >
          <dl className="space-y-2">
            <div>
              <dt className="font-semibold">User ID:</dt>
              <dd className="text-gray-600">{user.id}</dd>
            </div>
            <div>
              <dt className="font-semibold">Role:</dt>
              <dd className="text-gray-600">{user.role}</dd>
            </div>
          </dl>
        </div>
      )}

      {/* Actions */}
      {renderActions()}

      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
        </div>
      )}
    </div>
  );
};

// Example usage
export const UserCardExample: React.FC = () => {
  const exampleUser: User = {
    id: '123',
    name: 'Jane Doe',
    email: 'jane@example.com',
    role: 'admin',
    avatar: 'https://example.com/avatar.jpg',
  };

  const handleEdit = (user: User) => {
    console.log('Editing user:', user);
  };

  const handleDelete = (userId: string) => {
    console.log('Deleting user:', userId);
  };

  return (
    <UserCard
      user={exampleUser}
      onEdit={handleEdit}
      onDelete={handleDelete}
      showActions={true}
    />
  );
};
