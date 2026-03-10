# TypeScript Node.js CLI Template

Gold standard TypeScript CLI application template.

## Features

- Commander.js for argument parsing
- Chalk for colored output
- Ora for spinners
- Pino for structured logging
- Zod for configuration validation
- Vitest for testing

## Getting Started

```bash
# Install dependencies
npm install

# Development mode
npm run dev -- greet World

# Build
npm run build

# Run built CLI
npm start -- greet World

# Run tests
npm test
```

## Commands

```bash
# Greet command
mycli greet <name> [--loud]

# Process command
mycli process <files...> [--dry-run]
```

## Project Structure

```
src/
├── cli.ts           # CLI entry point
├── commands/        # Command implementations
│   ├── greet.ts
│   └── process.ts
├── config.ts        # Configuration
├── logger.ts        # Logging setup
└── utils.ts         # Utility functions
```
