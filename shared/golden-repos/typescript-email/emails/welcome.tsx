/**
 * Welcome email template.
 */

import { Text, Section, Link } from '@react-email/components';
import { Layout, Heading, Button } from '../src/components';

export interface WelcomeEmailProps {
  name: string;
  appUrl?: string;
}

export default function WelcomeEmail({
  name = 'there',
  appUrl = 'https://example.com',
}: WelcomeEmailProps) {
  return (
    <Layout preview={`Welcome to our platform, ${name}!`}>
      <Section style={styles.section}>
        <Heading>Welcome, {name}! 🎉</Heading>
        <Text style={styles.text}>
          Thanks for signing up! We're excited to have you on board.
        </Text>
        <Text style={styles.text}>
          Get started by exploring your dashboard and setting up your profile.
        </Text>
      </Section>
      <Section style={styles.buttonSection}>
        <Button href={`${appUrl}/dashboard`}>Go to Dashboard</Button>
      </Section>
      <Section style={styles.section}>
        <Text style={styles.text}>
          Need help?{' '}
          <Link href={`${appUrl}/help`} style={styles.link}>
            Visit our help center
          </Link>
          .
        </Text>
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
  link: {
    color: '#5046e5',
    textDecoration: 'underline',
  },
};
