# React Email Reference

**Type-safe, component-based email templates with excellent DX**

---

## Overview

React Email enables building beautiful, responsive emails using React components and TypeScript. Templates are rendered to production-ready HTML with inlined CSS.

**Why React Email:**
- ✅ Component-based architecture (DRY, reusable)
- ✅ Full TypeScript support with type-safe props
- ✅ Preview server with hot reload
- ✅ Automatic CSS inlining
- ✅ Used by Stripe, Vercel, Linear, Resend

---

## Setup

```bash
npm install react-email @react-email/components
```

**Development:**
```bash
npm run email dev
```

**Build for production:**
```bash
npm run email build
```

---

## Directory Structure

```
react-email/
├── templates/
│   ├── welcome.tsx              # Welcome email
│   ├── reset-password.tsx       # Password reset
│   ├── notification.tsx         # Generic notification
│   └── receipt.tsx              # Order receipt
├── components/
│   ├── EmailButton.tsx          # Reusable button component
│   ├── EmailHeader.tsx          # Header with logo
│   └── EmailFooter.tsx          # Footer with links
├── package.json
└── README.md
```

---

## Core Components

### @react-email/components

| Component | Purpose | Example |
|-----------|---------|---------|
| `<Html>` | Root wrapper | `<Html lang="en">` |
| `<Head>` | Document head | `<Head><title>Email</title></Head>` |
| `<Body>` | Email body | `<Body style={{ fontFamily: 'sans-serif' }}>` |
| `<Container>` | Max-width content wrapper | `<Container style={{ maxWidth: '600px' }}>` |
| `<Text>` | Paragraph text | `<Text>Hello {name}</Text>` |
| `<Button>` | CTA button | `<Button href={url}>Click Me</Button>` |
| `<Link>` | Inline link | `<Link href={url}>Read More</Link>` |
| `<Img>` | Image | `<Img src={url} alt="Logo" width={100} />` |
| `<Hr>` | Horizontal rule | `<Hr />` |
| `<Section>` | Layout section | `<Section>...</Section>` |
| `<Row>` & `<Column>` | Multi-column layouts | `<Row><Column>...</Column></Row>` |

---

## Pattern: Welcome Email

**File:** `templates/welcome.tsx`

```tsx
import { Button, Html, Head, Body, Container, Text, Img } from '@react-email/components';

interface WelcomeEmailProps {
  name: string;
  actionUrl: string;
  logoUrl?: string;
}

export default function WelcomeEmail({
  name,
  actionUrl,
  logoUrl = 'https://example.com/logo.png'
}: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Body style={styles.body}>
        <Container style={styles.container}>
          {/* Header */}
          <Img src={logoUrl} alt="Logo" width={120} style={styles.logo} />

          {/* Content */}
          <Text style={styles.heading}>Welcome, {name}!</Text>
          <Text style={styles.text}>
            Thanks for joining us. We're excited to have you on board.
          </Text>

          {/* CTA */}
          <Button href={actionUrl} style={styles.button}>
            Get Started
          </Button>

          {/* Footer */}
          <Text style={styles.footer}>
            Questions? Reply to this email or visit our help center.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

// Inline styles (required for email clients)
const styles = {
  body: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
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
  logo: {
    marginBottom: '24px',
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#232F3E',
    marginBottom: '16px',
  },
  text: {
    fontSize: '16px',
    lineHeight: '24px',
    color: '#333333',
    marginBottom: '24px',
  },
  button: {
    backgroundColor: '#FF9900',
    color: '#ffffff',
    padding: '12px 24px',
    borderRadius: '4px',
    textDecoration: 'none',
    display: 'inline-block',
    fontWeight: 'bold',
  },
  footer: {
    fontSize: '14px',
    color: '#666666',
    marginTop: '32px',
  },
};
```

---

## Pattern: Password Reset

**File:** `templates/reset-password.tsx`

```tsx
import { Button, Html, Head, Body, Container, Text, Link } from '@react-email/components';

interface ResetPasswordEmailProps {
  name: string;
  resetUrl: string;
  expiryHours: number;
}

export default function ResetPasswordEmail({
  name,
  resetUrl,
  expiryHours = 24
}: ResetPasswordEmailProps) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'sans-serif', backgroundColor: '#f4f4f4' }}>
        <Container style={{ padding: '40px', backgroundColor: '#fff', maxWidth: '600px' }}>
          <Text style={{ fontSize: '18px', fontWeight: 'bold' }}>
            Hi {name},
          </Text>

          <Text>
            We received a request to reset your password. Click the button below to create a new password:
          </Text>

          <Button
            href={resetUrl}
            style={{
              backgroundColor: '#FF9900',
              color: '#fff',
              padding: '12px 24px',
              borderRadius: '4px',
              textDecoration: 'none',
            }}
          >
            Reset Password
          </Button>

          <Text style={{ color: '#666', fontSize: '14px' }}>
            This link expires in {expiryHours} hours. If you didn't request this, you can safely ignore this email.
          </Text>

          <Text style={{ fontSize: '12px', color: '#999', marginTop: '32px' }}>
            Or copy and paste this URL: <Link href={resetUrl}>{resetUrl}</Link>
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

---

## Pattern: Notification Email

**File:** `templates/notification.tsx`

```tsx
import { Html, Head, Body, Container, Text, Section, Hr } from '@react-email/components';

type NotificationLevel = 'info' | 'success' | 'warning' | 'error';

interface NotificationEmailProps {
  title: string;
  message: string;
  level?: NotificationLevel;
  timestamp: string;
}

export default function NotificationEmail({
  title,
  message,
  level = 'info',
  timestamp
}: NotificationEmailProps) {
  const colors = {
    info: '#0066CC',
    success: '#00875A',
    warning: '#FF991F',
    error: '#DE350B',
  };

  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'sans-serif', backgroundColor: '#f4f4f4' }}>
        <Container style={{ padding: '40px', backgroundColor: '#fff', maxWidth: '600px' }}>
          <Section style={{ borderLeft: `4px solid ${colors[level]}`, paddingLeft: '16px' }}>
            <Text style={{ fontSize: '20px', fontWeight: 'bold', color: colors[level] }}>
              {title}
            </Text>
            <Text style={{ fontSize: '16px', lineHeight: '24px' }}>
              {message}
            </Text>
          </Section>

          <Hr style={{ margin: '24px 0', borderColor: '#e0e0e0' }} />

          <Text style={{ fontSize: '12px', color: '#999' }}>
            Sent at {timestamp}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

---

## Reusable Components

### EmailButton

**File:** `components/EmailButton.tsx`

```tsx
import { Button } from '@react-email/components';

interface EmailButtonProps {
  href: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

export default function EmailButton({
  href,
  children,
  variant = 'primary'
}: EmailButtonProps) {
  const styles = {
    primary: {
      backgroundColor: '#FF9900',
      color: '#ffffff',
    },
    secondary: {
      backgroundColor: '#232F3E',
      color: '#ffffff',
    },
  };

  return (
    <Button
      href={href}
      style={{
        ...styles[variant],
        padding: '12px 24px',
        borderRadius: '4px',
        textDecoration: 'none',
        display: 'inline-block',
        fontWeight: 'bold',
      }}
    >
      {children}
    </Button>
  );
}
```

---

## Best Practices

### 1. Type Safety
```tsx
// ✅ Define props interface
interface EmailProps {
  name: string;
  url: string;
  date?: Date;
}

export default function MyEmail({ name, url, date }: EmailProps) {
  // TypeScript ensures type safety
}
```

### 2. Inline Styles
```tsx
// ✅ Use inline styles (required for email clients)
<Text style={{ fontSize: '16px', color: '#333' }}>Hello</Text>

// ❌ Avoid external CSS (not supported)
<Text className="my-class">Hello</Text>
```

### 3. Responsive Design
```tsx
// ✅ Use max-width for responsive containers
<Container style={{ maxWidth: '600px', width: '100%' }}>
  {/* Content */}
</Container>
```

### 4. Images
```tsx
// ✅ Always include alt text and dimensions
<Img
  src="https://example.com/logo.png"
  alt="Company Logo"
  width={120}
  height={40}
/>

// ❌ Avoid relative paths
<Img src="/logo.png" alt="Logo" />
```

### 5. Testing
```bash
# Preview locally
npm run email dev

# Test across clients
# Use services like Litmus or Email on Acid for cross-client testing
```

---

## Sending with Resend

```typescript
import { Resend } from 'resend';
import WelcomeEmail from './templates/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'noreply@example.com',
  to: 'user@example.com',
  subject: 'Welcome to Our Platform',
  react: WelcomeEmail({
    name: 'John Doe',
    actionUrl: 'https://example.com/onboarding'
  }),
});
```

---

## Sending with AWS SES

```typescript
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';
import { render } from '@react-email/render';
import WelcomeEmail from './templates/welcome';

const ses = new SESClient({ region: 'us-east-1' });

const emailHtml = render(WelcomeEmail({
  name: 'John Doe',
  actionUrl: 'https://example.com/onboarding'
}));

await ses.send(new SendEmailCommand({
  Source: 'noreply@example.com',
  Destination: { ToAddresses: ['user@example.com'] },
  Message: {
    Subject: { Data: 'Welcome to Our Platform' },
    Body: { Html: { Data: emailHtml } },
  },
}));
```

---

## Resources

- **Official Docs:** https://react.email/docs/introduction
- **Examples:** https://react.email/examples
- **Components:** https://react.email/docs/components/html
- **GitHub:** https://github.com/resend/react-email

---

## Related

- `docs/system/DEVELOPMENT_STANDARDS.md` → Section 3.7 Email Standards
- `shared/tech-preferences/services.json` → email_templating category
- `shared/email/` → Production email templates (when implemented)
