/**
 * Tests for email templates.
 */

import { describe, it, expect } from 'vitest';
import { render } from '@react-email/components';
import WelcomeEmail from '../emails/welcome';
import PasswordResetEmail from '../emails/password-reset';
import NotificationEmail from '../emails/notification';

describe('WelcomeEmail', () => {
  it('renders with name', async () => {
    const html = await render(<WelcomeEmail name="John" />);
    expect(html).toContain('Welcome, John!');
    expect(html).toContain('Go to Dashboard');
  });

  it('includes preview text', async () => {
    const html = await render(<WelcomeEmail name="Jane" />);
    expect(html).toContain('Welcome to our platform, Jane!');
  });
});

describe('PasswordResetEmail', () => {
  it('renders reset link', async () => {
    const html = await render(
      <PasswordResetEmail resetUrl="https://example.com/reset/abc123" />
    );
    expect(html).toContain('Reset Your Password');
    expect(html).toContain('https://example.com/reset/abc123');
  });

  it('shows expiration time', async () => {
    const html = await render(
      <PasswordResetEmail resetUrl="https://example.com" expiresIn="30 minutes" />
    );
    expect(html).toContain('30 minutes');
  });
});

describe('NotificationEmail', () => {
  it('renders title and message', async () => {
    const html = await render(
      <NotificationEmail
        title="New Comment"
        message="Someone commented on your post."
      />
    );
    expect(html).toContain('New Comment');
    expect(html).toContain('Someone commented on your post.');
  });

  it('renders action button when provided', async () => {
    const html = await render(
      <NotificationEmail
        title="Test"
        message="Test message"
        actionUrl="https://example.com/action"
        actionText="Take Action"
      />
    );
    expect(html).toContain('Take Action');
    expect(html).toContain('https://example.com/action');
  });
});
