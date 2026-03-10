import { forwardRef, type HTMLAttributes, type ReactNode } from 'react';
import { cn } from '../utils/cn';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** Card header content */
  header?: ReactNode;
  /** Card footer content */
  footer?: ReactNode;
  /** Remove default padding */
  noPadding?: boolean;
}

/**
 * Card container for grouping related content.
 *
 * @example
 * ```tsx
 * <Card header={<h2>Title</h2>} footer={<Button>Action</Button>}>
 *   Card content here
 * </Card>
 * ```
 */
export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ header, footer, noPadding, children, className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'bg-white rounded-lg border border-gray-200 shadow-sm',
          className
        )}
        {...props}
      >
        {header && (
          <div className="px-4 py-3 border-b border-gray-200 font-medium">
            {header}
          </div>
        )}
        <div className={noPadding ? '' : 'p-4'}>{children}</div>
        {footer && (
          <div className="px-4 py-3 border-t border-gray-200 bg-gray-50 rounded-b-lg">
            {footer}
          </div>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';
