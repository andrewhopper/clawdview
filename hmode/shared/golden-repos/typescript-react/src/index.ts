/**
 * React Component Library - Public API
 */

// Configuration
export { configure, getConfig, isProduction, isLocal } from './config';
export type { LibraryConfig, Environment } from './config';

// Components
export { Button } from './components/Button';
export type { ButtonProps } from './components/Button';

export { Card } from './components/Card';
export type { CardProps } from './components/Card';

export { Input } from './components/Input';
export type { InputProps } from './components/Input';

// Hooks
export { useToggle } from './hooks/useToggle';
export { useDebounce } from './hooks/useDebounce';
export { useLocalStorage } from './hooks/useLocalStorage';

// Utils
export { cn } from './utils/cn';
export { formatDate, truncate } from './utils/format';
