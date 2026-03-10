/**
 * AWS Cloudscape Design System for Protoflow
 *
 * @packageDocumentation
 * @module @protoflow/design-system-cloudscape
 *
 * AWS Cloudscape is a design system for building intuitive, engaging,
 * and inclusive user experiences at scale.
 *
 * @see https://cloudscape.design/
 *
 * @example
 * ```tsx
 * import { AppLayout, Container, Header, Button } from '@protoflow/design-system-cloudscape';
 * import '@protoflow/design-system-cloudscape/globals.css';
 *
 * function App() {
 *   return (
 *     <AppLayout
 *       content={
 *         <Container header={<Header>My App</Header>}>
 *           <Button variant="primary">Click me</Button>
 *         </Container>
 *       }
 *     />
 *   );
 * }
 * ```
 */

// Re-export all components
export * from './components';

// Re-export utilities
export * from './lib/utils';
