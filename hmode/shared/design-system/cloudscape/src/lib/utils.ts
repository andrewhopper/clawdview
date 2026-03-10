/**
 * Cloudscape utility functions
 */

import type { NonCancelableCustomEvent } from '@cloudscape-design/components';

/**
 * Extract value from Cloudscape form field change events
 */
export function getEventDetail<T>(event: NonCancelableCustomEvent<T>): T {
  return event.detail;
}

/**
 * Create Cloudscape-compatible onChange handler
 */
export function createChangeHandler<T>(
  setter: (value: T) => void,
  key: keyof T & string = 'value' as keyof T & string
) {
  return (event: NonCancelableCustomEvent<T>) => {
    const detail = event.detail;
    setter((detail as Record<string, unknown>)[key] as T);
  };
}

/**
 * Format bytes to human readable string (for file upload components)
 */
export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Create breadcrumb items from path
 */
export function pathToBreadcrumbs(
  path: string,
  basePath = '/'
): Array<{ text: string; href: string }> {
  const segments = path.split('/').filter(Boolean);
  let currentPath = basePath;

  return [
    { text: 'Home', href: basePath },
    ...segments.map((segment) => {
      currentPath = `${currentPath}${segment}/`;
      return {
        text: segment.charAt(0).toUpperCase() + segment.slice(1),
        href: currentPath,
      };
    }),
  ];
}
