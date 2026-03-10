/**
 * Welcome Email Template
 *
 * Sent to new users upon account creation.
 *
 * @example
 * ```tsx
 * import WelcomeEmail from './templates/welcome';
 *
 * <WelcomeEmail
 *   name="John Doe"
 *   actionUrl="https://example.com/onboarding"
 *   logoUrl="https://example.com/logo.png"
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
  Img,
  Hr,
  Link,
  Section,
} from '@react-email/components';

export interface WelcomeEmailProps {
  /** User's display name */
  name: string;
  /** URL for the primary CTA button */
  actionUrl: string;
  /** Optional logo URL (defaults to example) */
  logoUrl?: string;
}

export default function WelcomeEmail({
  name,
  actionUrl,
  logoUrl = 'https://via.placeholder.com/120x40/232F3E/FFFFFF?text=Logo',
}: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Head>
        <title>Welcome to Our Platform</title>
      </Head>
      <Body style={styles.body}>
        <Container style={styles.container}>
          {/* Header with logo */}
          <Section style={styles.header}>
            <Img src={logoUrl} alt="Company Logo" width={120} style={styles.logo} />
          </Section>

          {/* Main content */}
          <Text style={styles.heading}>Welcome, {name}!</Text>

          <Text style={styles.text}>
            Thanks for joining our platform. We're excited to have you on board and can't wait to
            see what you'll build.
          </Text>

          <Text style={styles.text}>
            To get started, click the button below to complete your onboarding:
          </Text>

          {/* Primary CTA */}
          <Section style={styles.buttonContainer}>
            <Button href={actionUrl} style={styles.button}>
              Get Started
            </Button>
          </Section>

          <Hr style={styles.hr} />

          {/* Footer */}
          <Text style={styles.footer}>
            Questions? Reply to this email or visit our{' '}
            <Link href="https://example.com/help" style={styles.link}>
              help center
            </Link>
            .
          </Text>

          <Text style={styles.footerSmall}>
            You're receiving this email because you created an account on our platform.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

// Inline styles (required for email client compatibility)
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
  header: {
    marginBottom: '32px',
  },
  logo: {
    marginBottom: '0',
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold' as const,
    color: '#232F3E',
    marginBottom: '16px',
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
  hr: {
    borderColor: '#e0e0e0',
    margin: '32px 0',
  },
  footer: {
    fontSize: '14px',
    color: '#666666',
    marginBottom: '8px',
    lineHeight: '20px',
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
