/**
 * Generic Notification Email Template
 *
 * Multi-purpose notification template with severity levels.
 *
 * @example
 * ```tsx
 * import NotificationEmail from './templates/notification';
 *
 * <NotificationEmail
 *   title="Deployment Successful"
 *   message="Your application has been deployed to production."
 *   level="success"
 *   timestamp="2025-01-15 14:30 UTC"
 * />
 * ```
 */

import {
  Html,
  Head,
  Body,
  Container,
  Text,
  Section,
  Hr,
} from '@react-email/components';

export type NotificationLevel = 'info' | 'success' | 'warning' | 'error';

export interface NotificationEmailProps {
  /** Notification title */
  title: string;
  /** Notification message (supports basic formatting) */
  message: string;
  /** Severity level (affects color scheme) */
  level?: NotificationLevel;
  /** Timestamp string */
  timestamp: string;
  /** Optional metadata to display */
  metadata?: Record<string, string>;
}

export default function NotificationEmail({
  title,
  message,
  level = 'info',
  timestamp,
  metadata,
}: NotificationEmailProps) {
  const levelConfig = getLevelConfig(level);

  return (
    <Html lang="en">
      <Head>
        <title>{title}</title>
      </Head>
      <Body style={styles.body}>
        <Container style={styles.container}>
          {/* Title with colored border */}
          <Section
            style={{
              ...styles.titleSection,
              borderLeftColor: levelConfig.color,
            }}
          >
            <Text style={styles.levelLabel}>{levelConfig.emoji} {levelConfig.label}</Text>
            <Text style={{ ...styles.heading, color: levelConfig.color }}>{title}</Text>
          </Section>

          {/* Message */}
          <Text style={styles.message}>{message}</Text>

          {/* Optional metadata */}
          {metadata && Object.keys(metadata).length > 0 && (
            <Section style={styles.metadataSection}>
              <Text style={styles.metadataTitle}>Details:</Text>
              {Object.entries(metadata).map(([key, value]) => (
                <Text key={key} style={styles.metadataRow}>
                  <strong>{key}:</strong> {value}
                </Text>
              ))}
            </Section>
          )}

          <Hr style={styles.hr} />

          {/* Footer */}
          <Text style={styles.timestamp}>Sent at {timestamp}</Text>
          <Text style={styles.footer}>
            This is an automated notification. Please do not reply to this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

// Level configuration
function getLevelConfig(level: NotificationLevel) {
  const configs = {
    info: {
      label: 'Information',
      color: '#0066CC',
      emoji: 'ℹ️',
    },
    success: {
      label: 'Success',
      color: '#00875A',
      emoji: '✅',
    },
    warning: {
      label: 'Warning',
      color: '#FF991F',
      emoji: '⚠️',
    },
    error: {
      label: 'Error',
      color: '#DE350B',
      emoji: '❌',
    },
  };

  return configs[level];
}

const styles = {
  body: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace',
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
  titleSection: {
    borderLeft: '4px solid',
    paddingLeft: '16px',
    marginBottom: '24px',
  },
  levelLabel: {
    fontSize: '12px',
    fontWeight: 'bold' as const,
    textTransform: 'uppercase' as const,
    color: '#666666',
    marginBottom: '4px',
    marginTop: '0',
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold' as const,
    marginTop: '0',
    marginBottom: '0',
  },
  message: {
    fontSize: '16px',
    lineHeight: '24px',
    color: '#333333',
    marginBottom: '24px',
    whiteSpace: 'pre-wrap' as const,
  },
  metadataSection: {
    backgroundColor: '#F5F5F5',
    borderRadius: '4px',
    padding: '16px',
    marginBottom: '24px',
  },
  metadataTitle: {
    fontSize: '14px',
    fontWeight: 'bold' as const,
    color: '#333333',
    marginBottom: '8px',
    marginTop: '0',
  },
  metadataRow: {
    fontSize: '14px',
    color: '#666666',
    margin: '4px 0',
    fontFamily: 'monospace',
  },
  hr: {
    borderColor: '#e0e0e0',
    margin: '24px 0',
  },
  timestamp: {
    fontSize: '12px',
    color: '#999999',
    marginBottom: '8px',
  },
  footer: {
    fontSize: '12px',
    color: '#999999',
    marginTop: '4px',
  },
};
