# TypeScript Reference Example

## Overview
Gold standard TypeScript code demonstrating best practices for type-safe development.

## Key Features

### Type Safety
- Explicit interface definitions
- Generic types for reusability
- Proper type guards and narrowing

### Error Handling
- Custom error classes
- Try-catch with typed errors
- Result types for safe error propagation

### Documentation
- JSDoc comments for all public APIs
- Type annotations for clarity
- Usage examples

### Async Patterns
- Proper async/await usage
- Timeout handling with Promise.race
- Batch processing with Promise.all

## Files
- `data-processor.ts` - Complete TypeScript module with types, validation, and async processing

## Usage
```typescript
import { processDataItem, processBatch, DataItem } from './data-processor';

const item: DataItem = { id: '1', value: 42 };
const result = await processDataItem(item, { validate: true });
```

## Standards Demonstrated
- **Naming:** PascalCase for types/classes, camelCase for functions/variables
- **Exports:** Named exports preferred over default exports
- **Error handling:** Custom error classes with proper inheritance
- **Async:** Always use async/await, never raw promises
- **Types:** Explicit return types on all functions
