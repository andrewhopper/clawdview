/**
 * Email Domain Model - TypeScript Types
 * Generated from: shared/domain-models/email/ontology.ttl
 * Version: 1.0.0
 * Standards: W3C RDF, OWL, SHACL
 *
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * To regenerate: /generate-domain email --lang typescript
 */

// ============================================
// Entity Types
// ============================================

/**
 * Electronic mail message
 */
export interface Email {
  /** Unique identifier */
  id: string;

  /** Email subject line (1-998 characters per RFC 2822) */
  subject: string;

  /** Email body content */
  body: string;

  /** Email recipient addresses (To field) */
  recipients: string[];

  /** Carbon copy recipients */
  cc?: string[];

  /** Blind carbon copy recipients */
  bcc?: string[];

  /** Person who sent the email */
  sender: string;

  /** Current status of email */
  status: EmailStatus;

  /** Whether email has been read */
  isRead: boolean;

  /** Timestamp when email was sent */
  sentAt?: Date;

  /** Timestamp when email was read */
  readAt?: Date;

  /** Timestamp when email was deleted */
  deletedAt?: Date;

  /** File attachments */
  attachments?: EmailAttachment[];
}

/**
 * Container for received emails
 */
export interface Inbox {
  /** Unique identifier */
  id: string;

  /** Emails in inbox */
  emails: Email[];
}

/**
 * Organizational folder for emails
 */
export interface EmailFolder {
  /** Unique identifier */
  id: string;

  /** Folder name */
  name: FolderName;

  /** Emails in folder */
  emails: Email[];
}

/**
 * Conversation thread of related emails
 */
export interface EmailThread {
  /** Unique identifier */
  id: string;

  /** Thread subject */
  subject: string;

  /** Emails in thread */
  emails: Email[];
}

/**
 * File attached to email
 */
export interface EmailAttachment {
  /** File name (1-255 characters) */
  filename: string;

  /** MIME content type */
  contentType: string;

  /** File size in bytes (1 byte - 25MB) */
  size: number;

  /** Download URL */
  url?: string;
}

// ============================================
// Enum Types
// ============================================

/**
 * Email Status
 * Current status of email message
 */
export enum EmailStatus {
  /** Composed but not sent */
  Draft = 'draft',

  /** Delivered to recipients */
  Sent = 'sent',

  /** Moved to trash */
  Deleted = 'deleted',

  /** Long-term storage */
  Archived = 'archived',
}

/**
 * Folder Name
 * Standard email folder names
 */
export enum FolderName {
  /** Received messages */
  Inbox = 'inbox',

  /** Sent messages */
  Sent = 'sent',

  /** Unsent drafts */
  Drafts = 'drafts',

  /** Deleted messages */
  Trash = 'trash',

  /** Archived messages */
  Archive = 'archive',
}

// ============================================
// Action Input Types
// ============================================

/**
 * Input for SendEmailAction
 */
export interface SendEmailInput {
  /** Recipient email addresses (To field) */
  to: string[];

  /** Email subject line */
  subject: string;

  /** Email body content (plain text or HTML) */
  body: string;

  /** CC recipients (optional) */
  cc?: string[];

  /** BCC recipients (optional) */
  bcc?: string[];

  /** File attachments (optional) */
  attachments?: EmailAttachment[];
}

/**
 * Input for DeleteEmailAction
 */
export interface DeleteEmailInput {
  /** ID of email to delete */
  emailId: string;

  /** If true, permanently delete; if false, move to Trash */
  permanent?: boolean;
}

/**
 * Input for ForwardEmailAction
 */
export interface ForwardEmailInput {
  /** ID of email to forward */
  emailId: string;

  /** New recipient email addresses */
  to: string[];

  /** Optional message to prepend to forwarded content */
  message?: string;
}

/**
 * Input for MarkAsReadAction
 */
export interface MarkAsReadInput {
  /** ID of email to mark as read */
  emailId: string;
}

/**
 * Input for ArchiveEmailAction
 */
export interface ArchiveEmailInput {
  /** ID of email to archive */
  emailId: string;
}

/**
 * Input for SearchEmailsAction
 */
export interface SearchEmailsInput {
  /** Search query string */
  query: string;

  /** Limit search to specific folder */
  folder?: string;

  /** Search emails from this date onward */
  dateFrom?: Date;

  /** Search emails up to this date */
  dateTo?: Date;
}

// ============================================
// Validation Functions
// ============================================

/**
 * Validate email address format per RFC 5322
 */
export function isValidEmailAddress(email: string): boolean {
  const pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return pattern.test(email);
}

/**
 * Validate email subject per RFC 2822 (1-998 characters)
 */
export function isValidSubject(subject: string): boolean {
  return subject.length >= 1 && subject.length <= 998;
}

/**
 * Validate attachment size (1 byte - 25MB)
 */
export function isValidAttachmentSize(size: number): boolean {
  return size >= 1 && size <= 26214400; // 25MB in bytes
}

/**
 * Validate attachment filename (1-255 characters)
 */
export function isValidFilename(filename: string): boolean {
  return filename.length >= 1 && filename.length <= 255;
}

/**
 * Validate MIME content type
 */
export function isValidContentType(contentType: string): boolean {
  const pattern = /^[a-z]+\/[a-z0-9.+-]+$/;
  return pattern.test(contentType);
}

/**
 * Validate Email entity per SHACL constraints
 */
export function validateEmail(email: Email): ValidationResult {
  const errors: string[] = [];

  // Subject is required, 1-998 characters
  if (!email.subject || !isValidSubject(email.subject)) {
    errors.push('Subject is required and must be between 1-998 characters per RFC 2822');
  }

  // Body is required
  if (!email.body || email.body.length === 0) {
    errors.push('Email body is required and must not be empty');
  }

  // At least one recipient is required
  if (!email.recipients || email.recipients.length === 0) {
    errors.push('At least one valid recipient email address is required');
  }

  // Validate all recipient email addresses
  if (email.recipients) {
    for (const recipient of email.recipients) {
      if (!isValidEmailAddress(recipient)) {
        errors.push(`Invalid recipient email address: ${recipient}`);
      }
    }
  }

  // Validate CC addresses if present
  if (email.cc) {
    for (const cc of email.cc) {
      if (!isValidEmailAddress(cc)) {
        errors.push(`Invalid CC email address: ${cc}`);
      }
    }
  }

  // Validate BCC addresses if present
  if (email.bcc) {
    for (const bcc of email.bcc) {
      if (!isValidEmailAddress(bcc)) {
        errors.push(`Invalid BCC email address: ${bcc}`);
      }
    }
  }

  // Status is required
  if (!email.status) {
    errors.push('Status must be one of: Draft, Sent, Deleted, Archived');
  }

  // Sent emails must have sentAt timestamp
  if (email.status === EmailStatus.Sent && !email.sentAt) {
    errors.push('Emails with status "Sent" must have a sentAt timestamp');
  }

  // Read emails must have readAt timestamp
  if (email.isRead && !email.readAt) {
    errors.push('Emails marked as read (isRead=true) must have a readAt timestamp');
  }

  // Validate attachments if present
  if (email.attachments) {
    for (const attachment of email.attachments) {
      if (!isValidFilename(attachment.filename)) {
        errors.push(`Invalid attachment filename: ${attachment.filename} (must be 1-255 characters)`);
      }
      if (!isValidContentType(attachment.contentType)) {
        errors.push(`Invalid content type: ${attachment.contentType} (must be valid MIME type)`);
      }
      if (!isValidAttachmentSize(attachment.size)) {
        errors.push(`Invalid attachment size: ${attachment.size} bytes (must be 1 byte - 25MB)`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate EmailFolder entity per SHACL constraints
 */
export function validateEmailFolder(folder: EmailFolder): ValidationResult {
  const errors: string[] = [];

  // Folder name is required
  if (!folder.name) {
    errors.push('Folder name must be one of: inbox, sent, drafts, trash, archive');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate EmailThread entity per SHACL constraints
 */
export function validateEmailThread(thread: EmailThread): ValidationResult {
  const errors: string[] = [];

  // Thread must contain at least one email
  if (!thread.emails || thread.emails.length === 0) {
    errors.push('Thread must contain at least one email');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

// ============================================
// Utility Types
// ============================================

/**
 * Validation result
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Result type for operations that can fail
 */
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// ============================================
// Constants
// ============================================

/** RFC 2822 subject line max length */
export const MAX_SUBJECT_LENGTH = 998;

/** Email attachment max size (25MB) */
export const MAX_ATTACHMENT_SIZE = 26214400;

/** Filename max length */
export const MAX_FILENAME_LENGTH = 255;

/** Valid folder names */
export const VALID_FOLDER_NAMES: readonly FolderName[] = [
  FolderName.Inbox,
  FolderName.Sent,
  FolderName.Drafts,
  FolderName.Trash,
  FolderName.Archive,
] as const;

/** Valid email statuses */
export const VALID_EMAIL_STATUSES: readonly EmailStatus[] = [
  EmailStatus.Draft,
  EmailStatus.Sent,
  EmailStatus.Deleted,
  EmailStatus.Archived,
] as const;
