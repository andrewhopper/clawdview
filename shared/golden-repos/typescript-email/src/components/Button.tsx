/**
 * Email button component.
 */

import { Button as EmailButton } from '@react-email/components';

export interface ButtonProps {
  href: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
}

export function Button({ href, children, variant = 'primary' }: ButtonProps) {
  const variantStyles = {
    primary: {
      backgroundColor: '#5046e5',
      color: '#ffffff',
    },
    secondary: {
      backgroundColor: '#6b7280',
      color: '#ffffff',
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#5046e5',
      border: '1px solid #5046e5',
    },
  };

  return (
    <EmailButton
      href={href}
      style={{
        ...styles.button,
        ...variantStyles[variant],
      }}
    >
      {children}
    </EmailButton>
  );
}

const styles = {
  button: {
    borderRadius: '6px',
    fontSize: '16px',
    fontWeight: '600' as const,
    textDecoration: 'none',
    textAlign: 'center' as const,
    display: 'inline-block',
    padding: '12px 24px',
  },
};
