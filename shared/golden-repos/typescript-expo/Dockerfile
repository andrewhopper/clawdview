# syntax=docker/dockerfile:1
# Expo Dockerfile for CI/CD and EAS builds
FROM node:20 AS base

# Install Expo CLI
RUN npm install -g expo-cli eas-cli

# --- Dependencies stage ---
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- CI stage (for testing) ---
FROM base AS ci
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Run tests
CMD ["npm", "test"]

# --- Web build stage ---
FROM base AS web-build
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npx expo export --platform web

# --- Web production stage ---
FROM nginx:alpine AS web-prod

COPY --from=web-build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
