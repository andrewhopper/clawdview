/**
 * Email sending service using Resend.
 */

import { Resend } from 'resend';
import { render } from '@react-email/components';
import type { ReactElement } from 'react';
import { getConfig, getFromAddress } from './config';

export interface SendEmailOptions {
  to: string | string[];
  subject: string;
  react: ReactElement;
  from?: string;
  cc?: string | string[];
  bcc?: string | string[];
  replyTo?: string;
  tags?: Array<{ name: string; value: string }>;
}

export interface SendEmailResult {
  success: boolean;
  id?: string;
  error?: string;
}

let resendClient: Resend | null = null;

function getResendClient(): Resend {
  if (!resendClient) {
    const config = getConfig();
    resendClient = new Resend(config.RESEND_API_KEY);
  }
  return resendClient;
}

/**
 * Send an email using a React Email template.
 */
export async function sendEmail(options: SendEmailOptions): Promise<SendEmailResult> {
  const { to, subject, react, from, cc, bcc, replyTo, tags } = options;

  try {
    const resend = getResendClient();
    const html = await render(react);

    const { data, error } = await resend.emails.send({
      from: from ?? getFromAddress(),
      to: Array.isArray(to) ? to : [to],
      subject,
      html,
      cc: cc ? (Array.isArray(cc) ? cc : [cc]) : undefined,
      bcc: bcc ? (Array.isArray(bcc) ? bcc : [bcc]) : undefined,
      replyTo,
      tags,
    });

    if (error) {
      console.error('Failed to send email:', error);
      return { success: false, error: error.message };
    }

    console.log('Email sent successfully:', data?.id);
    return { success: true, id: data?.id };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error('Email send error:', message);
    return { success: false, error: message };
  }
}

/**
 * Render an email template to HTML string.
 */
export async function renderEmail(react: ReactElement): Promise<string> {
  return render(react);
}

/**
 * Render an email template to plain text.
 */
export async function renderEmailText(react: ReactElement): Promise<string> {
  return render(react, { plainText: true });
}
