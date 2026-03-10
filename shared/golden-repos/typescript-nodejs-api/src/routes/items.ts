/**
 * Items CRUD routes with Swagger annotations.
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { getLogger } from '../logger.js';
import { generateId } from '../utils.js';

export const itemsRouter = Router();
const log = getLogger('items');

// In-memory store (replace with database)
const items = new Map<string, Item>();

// Schemas
const ItemCreateSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
});

interface Item {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * @openapi
 * components:
 *   schemas:
 *     Item:
 *       type: object
 *       properties:
 *         id:
 *           type: string
 *           example: abc12345
 *         name:
 *           type: string
 *           example: My Item
 *         description:
 *           type: string
 *           example: A description of the item
 *         createdAt:
 *           type: string
 *           format: date-time
 *         updatedAt:
 *           type: string
 *           format: date-time
 *     ItemCreate:
 *       type: object
 *       required:
 *         - name
 *       properties:
 *         name:
 *           type: string
 *           minLength: 1
 *           maxLength: 100
 *         description:
 *           type: string
 *           maxLength: 500
 */

/**
 * @openapi
 * /api/items:
 *   post:
 *     tags:
 *       - Items
 *     summary: Create a new item
 *     description: Creates a new item with the provided name and optional description
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/ItemCreate'
 *     responses:
 *       201:
 *         description: Item created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Item'
 *       400:
 *         description: Validation error
 */
itemsRouter.post('/items', (req: Request, res: Response) => {
  const result = ItemCreateSchema.safeParse(req.body);
  if (!result.success) {
    res.status(400).json({ error: result.error.issues });
    return;
  }

  const now = new Date().toISOString();
  const item: Item = {
    id: generateId(),
    name: result.data.name,
    description: result.data.description,
    createdAt: now,
    updatedAt: now,
  };

  items.set(item.id, item);
  log.info({ itemId: item.id }, 'Item created');
  res.status(201).json(item);
});

/**
 * @openapi
 * /api/items:
 *   get:
 *     tags:
 *       - Items
 *     summary: List all items
 *     description: Returns a paginated list of all items
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           minimum: 1
 *           default: 1
 *         description: Page number
 *       - in: query
 *         name: pageSize
 *         schema:
 *           type: integer
 *           minimum: 1
 *           maximum: 100
 *           default: 10
 *         description: Items per page
 *     responses:
 *       200:
 *         description: List of items
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 items:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Item'
 *                 total:
 *                   type: integer
 *                 page:
 *                   type: integer
 *                 pageSize:
 *                   type: integer
 *                 hasNext:
 *                   type: boolean
 */
itemsRouter.get('/items', (req: Request, res: Response) => {
  const page = Math.max(1, parseInt(req.query.page as string) || 1);
  const pageSize = Math.min(100, Math.max(1, parseInt(req.query.pageSize as string) || 10));

  const allItems = Array.from(items.values());
  const total = allItems.length;
  const start = (page - 1) * pageSize;
  const pageItems = allItems.slice(start, start + pageSize);

  res.json({
    items: pageItems,
    total,
    page,
    pageSize,
    hasNext: start + pageSize < total,
  });
});

/**
 * @openapi
 * /api/items/{id}:
 *   get:
 *     tags:
 *       - Items
 *     summary: Get an item by ID
 *     description: Returns a single item by its unique identifier
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Item ID
 *     responses:
 *       200:
 *         description: Item found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Item'
 *       404:
 *         description: Item not found
 */
itemsRouter.get('/items/:id', (req: Request, res: Response) => {
  const item = items.get(req.params.id);
  if (!item) {
    res.status(404).json({ error: 'Item not found' });
    return;
  }
  res.json(item);
});

/**
 * @openapi
 * /api/items/{id}:
 *   delete:
 *     tags:
 *       - Items
 *     summary: Delete an item
 *     description: Permanently deletes an item by its unique identifier
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Item ID
 *     responses:
 *       204:
 *         description: Item deleted successfully
 *       404:
 *         description: Item not found
 */
itemsRouter.delete('/items/:id', (req: Request, res: Response) => {
  if (!items.has(req.params.id)) {
    res.status(404).json({ error: 'Item not found' });
    return;
  }
  items.delete(req.params.id);
  log.info({ itemId: req.params.id }, 'Item deleted');
  res.status(204).send();
});
