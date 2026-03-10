# syntax=docker/dockerfile:1
FROM node:20-alpine AS base

# --- Dependencies stage ---
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- Development stage (for email preview) ---
FROM base AS dev
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE 3000
CMD ["npx", "react-email", "dev"]

# --- Build stage ---
FROM base AS build
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build
