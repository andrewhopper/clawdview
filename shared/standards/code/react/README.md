# React Reference Example

## Overview
Gold standard React component with TypeScript, demonstrating modern React patterns.

## Key Features

### Component Structure
- Functional component with TypeScript
- Props interface with clear types
- Proper component composition

### React Hooks
- `useState` for local state management
- `useEffect` for side effects and cleanup
- `useCallback` for memoized callbacks

### TypeScript Integration
- Strict prop types
- State interfaces
- Generic components support

### Best Practices
- Accessibility (ARIA labels, semantic HTML)
- Conditional rendering
- Event handler patterns
- Loading and error states
- Component composition

## Files
- `UserCard.tsx` - Complete React component with TypeScript

## Usage
```tsx
import { UserCard, User } from './UserCard';

const user: User = {
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
  role: 'admin',
};

<UserCard
  user={user}
  onEdit={handleEdit}
  onDelete={handleDelete}
  showActions={true}
/>
```

## Standards Demonstrated
- **Props:** Interface-based with optional props and defaults
- **State:** Consolidated state object vs multiple useState
- **Handlers:** Memoized with useCallback
- **Rendering:** Helper functions for complex renders
- **Accessibility:** Proper ARIA attributes and semantic HTML
- **Styling:** Tailwind CSS classes (example, adaptable)
