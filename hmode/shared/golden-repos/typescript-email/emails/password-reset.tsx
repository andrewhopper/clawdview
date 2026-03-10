/**
 * Password reset email template.
 */

import { Text, Section, Code } from '@react-email/components';
import { Layout, Heading, Button } from '../src/components';

export interface PasswordResetEmailProps {
  name?: string;
  resetUrl: string;
  expiresIn?: string;
}

export default function PasswordResetEmail({
  name = 'there',
  resetUrl = 'https://example.com/reset',
  expiresIn = '1 hour',
}: PasswordResetEmailProps) {
  return (
    <Layout preview="Reset your password">
      <Section style={styles.section}>
        <Heading>Reset Your Password</Heading>
        <Text style={styles.text}>Hi {name},</Text>
        <Text style={styles.text}>
          We received a request to reset your password. Click the button below
          to create a new password.
        </Text>
      </Section>
      <Section style={styles.buttonSection}>
        <Button href={resetUrl}>Reset Password</Button>
      </Section>
      <Section style={styles.section}>
        <Text style={styles.text}>
          This link will expire in <strong>{expiresIn}</strong>.
        </Text>
        <Text style={styles.text}>
          If you didn't request a password reset, you can safely ignore this
          email.
        </Text>
        <Text style={styles.smallText}>
          Or copy and paste this URL into your browser:
        </Text>
        <Code style={styles.code}>{resetUrl}</Code>
      </Section>
    </Layout>
  );
}

const styles = {
  section: {
    padding: '0 24px',
  },
  buttonSection: {
    padding: '16px 24px',
    textAlign: 'center' as const,
  },
  text: {
    color: '#374151',
    fontSize: '16px',
    lineHeight: '24px',
    margin: '0 0 16px',
  },
  smallText: {
    color: '#6b7280',
    fontSize: '14px',
    lineHeight: '20px',
    margin: '0 0 8px',
  },
  code: {
    backgroundColor: '#f3f4f6',
    borderRadius: '4px',
    color: '#374151',
    display: 'block',
    fontSize: '12px',
    padding: '12px',
    wordBreak: 'break-all' as const,
  },
};
