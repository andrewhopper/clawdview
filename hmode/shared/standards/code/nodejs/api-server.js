/**
 * API Server - Node.js/Express Reference Example
 *
 * Demonstrates:
 * - Express.js server setup
 * - Middleware patterns
 * - Router organization
 * - Error handling
 * - Request validation
 * - Async route handlers
 * - Security best practices
 */

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');

// Configuration
const config = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  corsOrigin: process.env.CORS_ORIGIN || '*',
};

// Custom error classes
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
    this.statusCode = 400;
  }
}

class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NotFoundError';
    this.statusCode = 404;
  }
}

// Middleware: Request logging
const requestLogger = (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: `${duration}ms`,
      timestamp: new Date().toISOString(),
    });
  });

  next();
};

// Middleware: Async error handler wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Middleware: Request validation
const validateRequest = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body);
  if (error) {
    throw new ValidationError(error.details[0].message);
  }
  next();
};

// Mock database
const database = {
  users: [
    { id: '1', name: 'Alice', email: 'alice@example.com', role: 'admin' },
    { id: '2', name: 'Bob', email: 'bob@example.com', role: 'user' },
  ],
};

// Service layer - Business logic
const userService = {
  /**
   * Get all users
   * @returns {Promise<Array>} Array of users
   */
  async getAll() {
    // Simulate async operation
    return new Promise((resolve) => {
      setTimeout(() => resolve(database.users), 100);
    });
  },

  /**
   * Get user by ID
   * @param {string} id - User ID
   * @returns {Promise<Object>} User object
   * @throws {NotFoundError} If user not found
   */
  async getById(id) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const user = database.users.find((u) => u.id === id);
        if (!user) {
          reject(new NotFoundError(`User with id ${id} not found`));
        } else {
          resolve(user);
        }
      }, 100);
    });
  },

  /**
   * Create new user
   * @param {Object} userData - User data
   * @returns {Promise<Object>} Created user
   */
  async create(userData) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newUser = {
          id: String(database.users.length + 1),
          ...userData,
        };
        database.users.push(newUser);
        resolve(newUser);
      }, 100);
    });
  },

  /**
   * Update user
   * @param {string} id - User ID
   * @param {Object} updates - Update data
   * @returns {Promise<Object>} Updated user
   * @throws {NotFoundError} If user not found
   */
  async update(id, updates) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const index = database.users.findIndex((u) => u.id === id);
        if (index === -1) {
          reject(new NotFoundError(`User with id ${id} not found`));
        } else {
          database.users[index] = { ...database.users[index], ...updates };
          resolve(database.users[index]);
        }
      }, 100);
    });
  },

  /**
   * Delete user
   * @param {string} id - User ID
   * @returns {Promise<void>}
   * @throws {NotFoundError} If user not found
   */
  async delete(id) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const index = database.users.findIndex((u) => u.id === id);
        if (index === -1) {
          reject(new NotFoundError(`User with id ${id} not found`));
        } else {
          database.users.splice(index, 1);
          resolve();
        }
      }, 100);
    });
  },
};

// Router setup
const createUserRouter = () => {
  const router = express.Router();

  // GET /api/users - List all users
  router.get(
    '/',
    asyncHandler(async (req, res) => {
      const users = await userService.getAll();
      res.json({
        success: true,
        data: users,
        count: users.length,
      });
    })
  );

  // GET /api/users/:id - Get user by ID
  router.get(
    '/:id',
    asyncHandler(async (req, res) => {
      const user = await userService.getById(req.params.id);
      res.json({
        success: true,
        data: user,
      });
    })
  );

  // POST /api/users - Create new user
  router.post(
    '/',
    asyncHandler(async (req, res) => {
      // Simple validation
      if (!req.body.name || !req.body.email) {
        throw new ValidationError('Name and email are required');
      }

      const newUser = await userService.create(req.body);
      res.status(201).json({
        success: true,
        data: newUser,
      });
    })
  );

  // PATCH /api/users/:id - Update user
  router.patch(
    '/:id',
    asyncHandler(async (req, res) => {
      const updatedUser = await userService.update(req.params.id, req.body);
      res.json({
        success: true,
        data: updatedUser,
      });
    })
  );

  // DELETE /api/users/:id - Delete user
  router.delete(
    '/:id',
    asyncHandler(async (req, res) => {
      await userService.delete(req.params.id);
      res.status(204).send();
    })
  );

  return router;
};

// Error handling middleware
const errorHandler = (err, req, res, next) => {
  console.error('Error:', {
    name: err.name,
    message: err.message,
    stack: config.nodeEnv === 'development' ? err.stack : undefined,
  });

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal server error';

  res.status(statusCode).json({
    success: false,
    error: {
      message,
      type: err.name,
      ...(config.nodeEnv === 'development' && { stack: err.stack }),
    },
  });
};

// Create and configure app
const createApp = () => {
  const app = express();

  // Security middleware
  app.use(helmet());
  app.use(cors({ origin: config.corsOrigin }));

  // Body parsing
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Custom middleware
  app.use(requestLogger);

  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    });
  });

  // API routes
  app.use('/api/users', createUserRouter());

  // 404 handler
  app.use((req, res) => {
    res.status(404).json({
      success: false,
      error: {
        message: 'Route not found',
        path: req.path,
      },
    });
  });

  // Error handler (must be last)
  app.use(errorHandler);

  return app;
};

// Server startup
const startServer = () => {
  const app = createApp();

  const server = app.listen(config.port, () => {
    console.log({
      message: 'Server started',
      port: config.port,
      environment: config.nodeEnv,
      timestamp: new Date().toISOString(),
    });
  });

  // Graceful shutdown
  const shutdown = (signal) => {
    console.log(`${signal} received, shutting down gracefully...`);
    server.close(() => {
      console.log('Server closed');
      process.exit(0);
    });

    // Force shutdown after 10 seconds
    setTimeout(() => {
      console.error('Forced shutdown after timeout');
      process.exit(1);
    }, 10000);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  return server;
};

// Export for testing
module.exports = {
  createApp,
  startServer,
  userService,
  ValidationError,
  NotFoundError,
};

// Start server if run directly
if (require.main === module) {
  startServer();
}
