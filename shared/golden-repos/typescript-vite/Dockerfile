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

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# --- Production stage ---
FROM nginx:alpine AS prod

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
