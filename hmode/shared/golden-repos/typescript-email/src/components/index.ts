/**
 * Export all email components.
 */

export { Layout } from './Layout';
export type { LayoutProps } from './Layout';

export { Button } from './Button';
export type { ButtonProps } from './Button';

export { Heading } from './Heading';
export type { HeadingProps } from './Heading';

// Re-export commonly used React Email components
export {
  Text,
  Link,
  Img,
  Section,
  Row,
  Column,
  Hr,
  Code,
} from '@react-email/components';
