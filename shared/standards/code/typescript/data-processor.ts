/**
 * Data Processor - TypeScript Reference Example
 *
 * Demonstrates:
 * - Proper TypeScript type definitions
 * - Error handling patterns
 * - JSDoc documentation
 * - Functional programming patterns
 * - Async/await best practices
 */

// Type definitions
export interface ProcessingOptions {
  validate?: boolean;
  transform?: boolean;
  timeout?: number;
}

export interface DataItem {
  id: string;
  value: number;
  metadata?: Record<string, unknown>;
}

export interface ProcessingResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: Date;
}

// Custom error classes
export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class ProcessingError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = 'ProcessingError';
  }
}

/**
 * Validates a data item
 * @param item - The data item to validate
 * @returns True if valid
 * @throws ValidationError if validation fails
 */
function validateDataItem(item: DataItem): boolean {
  if (!item.id || typeof item.id !== 'string') {
    throw new ValidationError('Invalid or missing id');
  }

  if (typeof item.value !== 'number' || isNaN(item.value)) {
    throw new ValidationError('Invalid value: must be a number');
  }

  return true;
}

/**
 * Transforms a data item
 * @param item - The data item to transform
 * @returns Transformed data item
 */
function transformDataItem(item: DataItem): DataItem {
  return {
    ...item,
    value: item.value * 2,
    metadata: {
      ...item.metadata,
      transformed: true,
      transformedAt: new Date().toISOString(),
    },
  };
}

/**
 * Processes a single data item with options
 * @param item - The data item to process
 * @param options - Processing options
 * @returns Processing result
 */
export async function processDataItem(
  item: DataItem,
  options: ProcessingOptions = {}
): Promise<ProcessingResult<DataItem>> {
  const { validate = true, transform = true, timeout = 5000 } = options;

  try {
    // Create timeout promise
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error('Processing timeout')), timeout);
    });

    // Processing logic
    const processingPromise = (async () => {
      let processedItem = { ...item };

      if (validate) {
        validateDataItem(processedItem);
      }

      if (transform) {
        processedItem = transformDataItem(processedItem);
      }

      return processedItem;
    })();

    // Race between processing and timeout
    const result = await Promise.race([processingPromise, timeoutPromise]);

    return {
      success: true,
      data: result,
      timestamp: new Date(),
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date(),
    };
  }
}

/**
 * Processes multiple data items in batch
 * @param items - Array of data items
 * @param options - Processing options
 * @returns Array of processing results
 */
export async function processBatch(
  items: DataItem[],
  options: ProcessingOptions = {}
): Promise<ProcessingResult<DataItem>[]> {
  return Promise.all(items.map((item) => processDataItem(item, options)));
}

/**
 * Filters successful results from batch processing
 * @param results - Array of processing results
 * @returns Array of successful data items
 */
export function filterSuccessful<T>(
  results: ProcessingResult<T>[]
): T[] {
  return results
    .filter((result) => result.success && result.data !== undefined)
    .map((result) => result.data as T);
}

// Example usage
if (require.main === module) {
  const exampleData: DataItem[] = [
    { id: '1', value: 10 },
    { id: '2', value: 20, metadata: { source: 'api' } },
    { id: '3', value: 30 },
  ];

  processBatch(exampleData, { validate: true, transform: true })
    .then((results) => {
      console.log('Processing Results:', results);
      const successful = filterSuccessful(results);
      console.log('Successful Items:', successful);
    })
    .catch((error) => {
      console.error('Batch processing failed:', error);
    });
}
