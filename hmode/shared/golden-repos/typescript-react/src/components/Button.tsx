/**
 * Button component following shadcn/ui patterns
 * See shared/design-system for full component library
 */
import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { cn } from '../utils/cn';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button variant style - matches shadcn/ui variants */
  variant?: 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'link';
  /** Button size */
  size?: 'sm' | 'default' | 'lg' | 'icon';
  /** Show loading spinner */
  loading?: boolean;
  /** Icon to show before text */
  leftIcon?: ReactNode;
  /** Icon to show after text */
  rightIcon?: ReactNode;
}

/**
 * Primary button component for user interactions.
 * Follows shadcn/ui design system patterns.
 *
 * @example
 * ```tsx
 * <Button variant="default" onClick={handleClick}>
 *   Click me
 * </Button>
 * ```
 */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'default',
      size = 'default',
      loading = false,
      disabled,
      leftIcon,
      rightIcon,
      children,
      className,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';

    const variants = {
      default: 'bg-primary text-primary-foreground hover:bg-primary/90',
      secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
      outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
      ghost: 'hover:bg-accent hover:text-accent-foreground',
      destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      link: 'text-primary underline-offset-4 hover:underline',
    };

    const sizes = {
      sm: 'h-9 rounded-md px-3',
      default: 'h-10 px-4 py-2',
      lg: 'h-11 rounded-md px-8',
      icon: 'h-10 w-10',
    };

    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      >
        {loading ? (
          <LoadingSpinner size={size} />
        ) : (
          <>
            {leftIcon}
            {children}
            {rightIcon}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

function LoadingSpinner({ size }: { size: 'sm' | 'default' | 'lg' | 'icon' }) {
  const sizeMap = { sm: 'h-3 w-3', default: 'h-4 w-4', lg: 'h-5 w-5', icon: 'h-4 w-4' };
  return (
    <svg
      className={cn('animate-spin', sizeMap[size])}
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>
  );
}
