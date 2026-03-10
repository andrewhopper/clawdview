/**
 * Email heading component.
 */

import { Heading as EmailHeading } from '@react-email/components';

export interface HeadingProps {
  children: React.ReactNode;
  as?: 'h1' | 'h2' | 'h3';
}

export function Heading({ children, as = 'h1' }: HeadingProps) {
  const sizeStyles = {
    h1: { fontSize: '24px', lineHeight: '32px' },
    h2: { fontSize: '20px', lineHeight: '28px' },
    h3: { fontSize: '16px', lineHeight: '24px' },
  };

  return (
    <EmailHeading as={as} style={{ ...styles.heading, ...sizeStyles[as] }}>
      {children}
    </EmailHeading>
  );
}

const styles = {
  heading: {
    color: '#1f2937',
    fontWeight: '600' as const,
    margin: '0 0 16px',
    padding: '0 24px',
  },
};
