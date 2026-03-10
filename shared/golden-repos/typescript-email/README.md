# TypeScript React Email Template

Gold standard template for building and sending beautiful emails with React Email.

## Features

- **React Email**: Build emails with React components
- **Resend Integration**: Easy email sending via Resend API
- **Type Safety**: Full TypeScript support
- **Preview Server**: Live preview during development
- **Reusable Components**: Layout, Button, Heading components
- **Testing**: Vitest for template testing

## Quick Start

```bash
# Install dependencies
npm install

# Start preview server
npm run dev

# Open http://localhost:3001 to preview emails
```

## Usage

### Sending Emails

```typescript
import { sendEmail } from './src';
import WelcomeEmail from './emails/welcome';

const result = await sendEmail({
  to: 'user@example.com',
  subject: 'Welcome!',
  react: <WelcomeEmail name="John" />,
});

if (result.success) {
  console.log('Email sent:', result.id);
}
```

### Creating New Templates

Create a new file in `emails/` directory:

```typescript
import { Layout, Heading, Button, Text, Section } from '../src/components';

interface MyEmailProps {
  name: string;
}

export default function MyEmail({ name }: MyEmailProps) {
  return (
    <Layout preview="Email preview text">
      <Section style={{ padding: '0 24px' }}>
        <Heading>Hello, {name}!</Heading>
        <Text>Your email content here.</Text>
      </Section>
      <Section style={{ padding: '16px 24px', textAlign: 'center' }}>
        <Button href="https://example.com">Click Me</Button>
      </Section>
    </Layout>
  );
}
```

### Export to HTML

```bash
# Export all emails to HTML files
npm run export
```

## Project Structure

```
typescript-email/
├── emails/
│   ├── welcome.tsx         # Welcome email
│   ├── password-reset.tsx  # Password reset
│   └── notification.tsx    # Generic notification
├── src/
│   ├── components/
│   │   ├── Layout.tsx      # Base email layout
│   │   ├── Button.tsx      # CTA button
│   │   ├── Heading.tsx     # Heading component
│   │   └── index.ts        # Component exports
│   ├── config.ts           # Configuration
│   ├── send.ts             # Sending functions
│   └── index.ts            # Main exports
├── tests/
│   └── emails.test.tsx     # Template tests
├── package.json
├── tsconfig.json
└── README.md
```

## Configuration

Set environment variables in `.env`:

```
RESEND_API_KEY=re_xxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
DEFAULT_FROM_NAME=Your App Name
APP_URL=https://yourapp.com
```
