"""
Data Processor - Python Reference Example

Demonstrates:
- Type hints (PEP 484)
- Dataclasses for structured data
- Context managers
- Exception handling
- Async/await patterns
- Logging
- Docstrings (Google style)
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Enums
class ProcessingStatus(Enum):
    """Status of processing operation."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Custom exceptions
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class ProcessingError(Exception):
    """Raised when data processing fails."""

    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause


# Data models
@dataclass
class DataItem:
    """Represents a single data item to be processed.

    Attributes:
        id: Unique identifier
        value: Numeric value
        metadata: Optional metadata dictionary
        created_at: Creation timestamp
    """
    id: str
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate data after initialization."""
        if not self.id:
            raise ValidationError("ID cannot be empty")
        if not isinstance(self.value, (int, float)):
            raise ValidationError("Value must be numeric")


@dataclass
class ProcessingResult:
    """Result of a processing operation.

    Attributes:
        success: Whether processing succeeded
        data: Processed data if successful
        error: Error message if failed
        status: Processing status
        timestamp: Result timestamp
    """
    success: bool
    status: ProcessingStatus
    timestamp: datetime = field(default_factory=datetime.now)
    data: Optional[DataItem] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'success': self.success,
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data.__dict__ if self.data else None,
            'error': self.error,
        }


# Validation functions
def validate_data_item(item: DataItem) -> bool:
    """Validate a data item.

    Args:
        item: The data item to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    if not item.id or not isinstance(item.id, str):
        raise ValidationError("Invalid or missing ID")

    if not isinstance(item.value, (int, float)):
        raise ValidationError("Value must be numeric")

    if item.value < 0:
        raise ValidationError("Value cannot be negative")

    return True


# Transformation functions
def transform_data_item(item: DataItem) -> DataItem:
    """Transform a data item.

    Args:
        item: The data item to transform

    Returns:
        Transformed data item
    """
    return DataItem(
        id=item.id,
        value=item.value * 2,
        metadata={
            **item.metadata,
            'transformed': True,
            'transformed_at': datetime.now().isoformat(),
            'original_value': item.value,
        },
        created_at=item.created_at,
    )


# Async processing
class DataProcessor:
    """Handles data processing operations with async support."""

    def __init__(self, timeout: float = 5.0, validate: bool = True):
        """Initialize processor.

        Args:
            timeout: Processing timeout in seconds
            validate: Whether to validate items
        """
        self.timeout = timeout
        self.validate = validate
        self.processed_count = 0

    @asynccontextmanager
    async def processing_context(self, item_id: str):
        """Context manager for processing operations.

        Args:
            item_id: ID of item being processed

        Yields:
            None
        """
        logger.info(f"Starting processing for item {item_id}")
        start_time = datetime.now()

        try:
            yield
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Completed processing for item {item_id} in {duration:.2f}s")

    async def process_item(
        self,
        item: DataItem,
        transform: bool = True
    ) -> ProcessingResult:
        """Process a single data item asynchronously.

        Args:
            item: The data item to process
            transform: Whether to transform the item

        Returns:
            Processing result
        """
        async with self.processing_context(item.id):
            try:
                # Validation
                if self.validate:
                    validate_data_item(item)

                # Simulate async processing
                await asyncio.sleep(0.1)

                # Transformation
                processed_item = transform_data_item(item) if transform else item

                # Update counter
                self.processed_count += 1

                return ProcessingResult(
                    success=True,
                    status=ProcessingStatus.COMPLETED,
                    data=processed_item,
                )

            except ValidationError as e:
                logger.error(f"Validation failed for item {item.id}: {e}")
                return ProcessingResult(
                    success=False,
                    status=ProcessingStatus.FAILED,
                    error=str(e),
                )
            except Exception as e:
                logger.error(f"Processing failed for item {item.id}: {e}")
                return ProcessingResult(
                    success=False,
                    status=ProcessingStatus.FAILED,
                    error=f"Unexpected error: {str(e)}",
                )

    async def process_batch(
        self,
        items: List[DataItem],
        transform: bool = True,
        concurrency: int = 10
    ) -> List[ProcessingResult]:
        """Process multiple items in batch with concurrency control.

        Args:
            items: List of data items
            transform: Whether to transform items
            concurrency: Maximum concurrent operations

        Returns:
            List of processing results
        """
        logger.info(f"Processing batch of {len(items)} items")

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrency)

        async def process_with_semaphore(item: DataItem) -> ProcessingResult:
            async with semaphore:
                return await self.process_item(item, transform)

        # Process all items concurrently
        results = await asyncio.gather(
            *[process_with_semaphore(item) for item in items],
            return_exceptions=True
        )

        # Convert exceptions to failed results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(
                    ProcessingResult(
                        success=False,
                        status=ProcessingStatus.FAILED,
                        error=str(result),
                    )
                )
            else:
                processed_results.append(result)

        logger.info(
            f"Batch processing complete: "
            f"{sum(1 for r in processed_results if r.success)}/{len(items)} succeeded"
        )

        return processed_results


# Helper functions
def filter_successful(results: List[ProcessingResult]) -> List[DataItem]:
    """Filter successful results and extract data.

    Args:
        results: List of processing results

    Returns:
        List of successfully processed items
    """
    return [r.data for r in results if r.success and r.data is not None]


def get_statistics(results: List[ProcessingResult]) -> Dict[str, Any]:
    """Get statistics from processing results.

    Args:
        results: List of processing results

    Returns:
        Dictionary with statistics
    """
    total = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total - successful

    return {
        'total': total,
        'successful': successful,
        'failed': failed,
        'success_rate': successful / total if total > 0 else 0,
    }


# Example usage
async def main():
    """Example usage of the data processor."""
    # Create sample data
    items = [
        DataItem(id='1', value=10.0),
        DataItem(id='2', value=20.0, metadata={'source': 'api'}),
        DataItem(id='3', value=30.0),
    ]

    # Process batch
    processor = DataProcessor(timeout=5.0, validate=True)
    results = await processor.process_batch(items, transform=True, concurrency=5)

    # Get successful items
    successful_items = filter_successful(results)

    # Print statistics
    stats = get_statistics(results)
    logger.info(f"Processing statistics: {stats}")
    logger.info(f"Successful items: {len(successful_items)}")

    # Print results
    for result in results:
        print(result.to_dict())


if __name__ == '__main__':
    asyncio.run(main())
