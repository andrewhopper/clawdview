/**
 * Base email layout component.
 */

import {
  Html,
  Head,
  Body,
  Container,
  Section,
  Text,
  Hr,
  Preview,
  Font,
} from '@react-email/components';
import type { ReactNode } from 'react';

export interface LayoutProps {
  preview?: string;
  children: ReactNode;
  footerText?: string;
}

export function Layout({ preview, children, footerText }: LayoutProps) {
  return (
    <Html>
      <Head>
        <Font
          fontFamily="Inter"
          fallbackFontFamily="Helvetica"
          webFont={{
            url: 'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff2',
            format: 'woff2',
          }}
          fontWeight={400}
          fontStyle="normal"
        />
      </Head>
      {preview && <Preview>{preview}</Preview>}
      <Body style={styles.body}>
        <Container style={styles.container}>
          {children}
          <Hr style={styles.hr} />
          <Section style={styles.footer}>
            <Text style={styles.footerText}>
              {footerText ?? `© ${new Date().getFullYear()} My Company. All rights reserved.`}
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}

const styles = {
  body: {
    backgroundColor: '#f6f9fc',
    fontFamily: 'Inter, Helvetica, Arial, sans-serif',
  },
  container: {
    backgroundColor: '#ffffff',
    margin: '0 auto',
    padding: '20px 0 48px',
    marginBottom: '64px',
    maxWidth: '600px',
  },
  hr: {
    borderColor: '#e6ebf1',
    margin: '20px 0',
  },
  footer: {
    padding: '0 24px',
  },
  footerText: {
    color: '#8898aa',
    fontSize: '12px',
    lineHeight: '16px',
  },
};
