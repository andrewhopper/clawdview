/**
 * Generic notification email template.
 */

import { Text, Section, Link } from '@react-email/components';
import { Layout, Heading, Button } from '../src/components';

export interface NotificationEmailProps {
  title: string;
  message: string;
  actionUrl?: string;
  actionText?: string;
}

export default function NotificationEmail({
  title = 'New Notification',
  message = 'You have a new notification.',
  actionUrl,
  actionText = 'View Details',
}: NotificationEmailProps) {
  return (
    <Layout preview={title}>
      <Section style={styles.section}>
        <Heading>{title}</Heading>
        <Text style={styles.text}>{message}</Text>
      </Section>
      {actionUrl && (
        <Section style={styles.buttonSection}>
          <Button href={actionUrl}>{actionText}</Button>
        </Section>
      )}
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
};
