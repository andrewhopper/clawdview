/**
 * Reusable Email Button Component
 *
 * Styled button following Protoflow design standards.
 *
 * @example
 * ```tsx
 * import EmailButton from '../components/EmailButton';
 *
 * <EmailButton href="https://example.com" variant="primary">
 *   Click Me
 * </EmailButton>
 * ```
 */

import { Button } from '@react-email/components';
import React from 'react';

export interface EmailButtonProps {
  /** Button URL */
  href: string;
  /** Button content */
  children: React.ReactNode;
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'outline';
  /** Optional full width */
  fullWidth?: boolean;
}

export default function EmailButton({
  href,
  children,
  variant = 'primary',
  fullWidth = false,
}: EmailButtonProps) {
  const variantStyles = {
    primary: {
      backgroundColor: '#FF9900',
      color: '#ffffff',
      border: 'none',
    },
    secondary: {
      backgroundColor: '#232F3E',
      color: '#ffffff',
      border: 'none',
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#FF9900',
      border: '2px solid #FF9900',
    },
  };

  return (
    <Button
      href={href}
      style={{
        ...variantStyles[variant],
        padding: '12px 24px',
        borderRadius: '4px',
        textDecoration: 'none',
        display: fullWidth ? 'block' : 'inline-block',
        width: fullWidth ? '100%' : 'auto',
        textAlign: 'center' as const,
        fontWeight: 'bold' as const,
        fontSize: '16px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {children}
    </Button>
  );
}
