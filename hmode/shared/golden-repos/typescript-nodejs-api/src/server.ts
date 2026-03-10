/**
 * Express server with Swagger documentation.
 */

import express, { Express, Request, Response } from 'express';
import swaggerUi from 'swagger-ui-express';
import pinoHttp from 'pino-http';

import { getConfig } from './config.js';
import { getLogger } from './logger.js';
import { swaggerSpec } from './swagger.js';
import { healthRouter } from './routes/health.js';
import { itemsRouter } from './routes/items.js';
import { requestIdMiddleware, errorHandler } from './middleware/index.js';

const config = getConfig();
const log = getLogger('server');

export function createServer(): Express {
  const app = express();

  // Core middleware
  app.use(express.json());
  app.use(requestIdMiddleware);
  app.use(pinoHttp({ logger: log }));

  // Swagger documentation
  app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
  app.get('/api/docs.json', (_req: Request, res: Response) => {
    res.json(swaggerSpec);
  });

  // Routes
  app.use('/api', healthRouter);
  app.use('/api', itemsRouter);

  // Error handler (must be last)
  app.use(errorHandler);

  return app;
}

export function startServer(): void {
  const app = createServer();
  const port = config.PORT || 3000;

  app.listen(port, () => {
    log.info({ port }, 'Server started');
    log.info(`Swagger docs available at http://localhost:${port}/api/docs`);
  });
}
