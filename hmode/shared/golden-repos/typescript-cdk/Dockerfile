# syntax=docker/dockerfile:1
# CDK Dockerfile for CI/CD pipelines
FROM node:20-alpine AS base

# Install AWS CDK CLI globally
RUN npm install -g aws-cdk

# --- Dependencies stage ---
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- Build & Synth stage ---
FROM base AS build
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Synthesize CDK app
RUN cdk synth

# --- CI/CD stage ---
FROM base AS ci
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Default command runs tests
CMD ["npm", "test"]
