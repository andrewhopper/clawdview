# syntax=docker/dockerfile:1
FROM node:20-alpine AS base

# --- Dependencies stage ---
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- Builder stage ---
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# --- Development stage ---
FROM base AS dev
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]

# --- Production stage ---
FROM base AS prod
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package*.json ./

USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"]
