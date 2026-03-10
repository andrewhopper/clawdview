/**
 * Main application entry point.
 */

import { getConfig } from './config';
import { logger } from './logger';
import { $, createElement, on } from './dom';
import { generateId } from './utils';

// Initialize application
function init(): void {
  const config = getConfig();
  logger.info('Application starting', { appName: config.APP_NAME });

  const app = $('#app');
  if (!app) {
    logger.error('App container not found');
    return;
  }

  // Create UI
  const header = createElement('h1', {}, [config.APP_NAME]);
  const description = createElement('p', { class: 'description' }, [
    'Gold standard TypeScript Vite template',
  ]);

  const button = createElement('button', { id: 'action-btn', class: 'btn' }, ['Click me']);

  const output = createElement('div', { id: 'output', class: 'output' }, []);

  app.appendChild(header);
  app.appendChild(description);
  app.appendChild(button);
  app.appendChild(output);

  // Add event listener
  on(button, 'click', () => {
    const id = generateId();
    logger.info('Button clicked', { id });

    const item = createElement('div', { class: 'item' }, [`Generated ID: ${id}`]);
    output.appendChild(item);
  });

  logger.info('Application initialized');
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
