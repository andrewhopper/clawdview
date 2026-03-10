/**
 * Main exports for the email package.
 */

// Configuration
export { getConfig, getFromAddress } from './config';
export type { Config } from './config';

// Sending
export { sendEmail, renderEmail, renderEmailText } from './send';
export type { SendEmailOptions, SendEmailResult } from './send';

// Components
export * from './components';
