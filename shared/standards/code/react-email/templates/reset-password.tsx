/**
 * Password Reset Email Template
 *
 * Sent when a user requests a password reset.
 *
 * @example
 * ```tsx
 * import ResetPasswordEmail from './templates/reset-password';
 *
 * <ResetPasswordEmail
 *   name="John Doe"
 *   resetUrl="https://example.com/reset?token=abc123"
 *   expiryHours={24}
 * />
 * ```
 */

import {
  Button,
  Html,
  Head,
  Body,
  Container,
  Text,
  Link,
  Hr,
  Section,
} from '@react-email/components';

export interface ResetPasswordEmailProps {
  /** User's display name */
  name: string;
  /** Password reset URL with token */
  resetUrl: string;
  /** Hours until the reset link expires */
  expiryHours?: number;
}

export default function ResetPasswordEmail({
  name,
  resetUrl,
  expiryHours = 24,
}: ResetPasswordEmailProps) {
  return (
    <Html lang="en">
      <Head>
        <title>Reset Your Password</title>
      </Head>
      <Body style={styles.body}>
        <Container style={styles.container}>
          <Text style={styles.heading}>Password Reset Request</Text>

          <Text style={styles.text}>Hi {name},</Text>

          <Text style={styles.text}>
            We received a request to reset your password. Click the button below to create a new
            password:
          </Text>

          {/* Primary CTA */}
          <Section style={styles.buttonContainer}>
            <Button href={resetUrl} style={styles.button}>
              Reset Password
            </Button>
          </Section>

          {/* Security notice */}
          <Section style={styles.warningBox}>
            <Text style={styles.warningText}>
              ⏰ This link expires in <strong>{expiryHours} hours</strong>.
            </Text>
            <Text style={styles.warningText}>
              🔒 If you didn't request this, you can safely ignore this email. Your password won't
              change.
            </Text>
          </Section>

          <Hr style={styles.hr} />

          {/* Fallback link */}
          <Text style={styles.footer}>
            Or copy and paste this URL into your browser:
          </Text>
          <Text style={styles.urlText}>
            <Link href={resetUrl} style={styles.link}>
              {resetUrl}
            </Link>
          </Text>

          <Text style={styles.footerSmall}>
            Need help? Contact support at support@example.com
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const styles = {
  body: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f4f4f4',
    padding: '20px',
  },
  container: {
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    padding: '40px',
    maxWidth: '600px',
    margin: '0 auto',
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold' as const,
    color: '#232F3E',
    marginBottom: '24px',
    marginTop: '0',
  },
  text: {
    fontSize: '16px',
    lineHeight: '24px',
    color: '#333333',
    marginBottom: '16px',
  },
  buttonContainer: {
    textAlign: 'center' as const,
    margin: '32px 0',
  },
  button: {
    backgroundColor: '#FF9900',
    color: '#ffffff',
    padding: '14px 28px',
    borderRadius: '4px',
    textDecoration: 'none',
    display: 'inline-block',
    fontWeight: 'bold' as const,
    fontSize: '16px',
  },
  warningBox: {
    backgroundColor: '#FFF3CD',
    border: '1px solid #FFE69C',
    borderRadius: '4px',
    padding: '16px',
    marginTop: '24px',
  },
  warningText: {
    fontSize: '14px',
    color: '#856404',
    margin: '4px 0',
  },
  hr: {
    borderColor: '#e0e0e0',
    margin: '32px 0',
  },
  footer: {
    fontSize: '14px',
    color: '#666666',
    marginBottom: '8px',
  },
  urlText: {
    fontSize: '12px',
    color: '#666666',
    wordBreak: 'break-all' as const,
    marginBottom: '24px',
  },
  footerSmall: {
    fontSize: '12px',
    color: '#999999',
    marginTop: '16px',
  },
  link: {
    color: '#FF9900',
    textDecoration: 'underline',
  },
};
