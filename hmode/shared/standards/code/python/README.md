# Python Reference Example

## Overview
Gold standard Python code demonstrating modern Python 3.8+ best practices.

## Key Features

### Type Hints
- Full PEP 484 type annotations
- Complex types (Union, Optional, List, Dict)
- Generic types
- Return type annotations

### Data Classes
- Structured data with @dataclass
- Default factories
- Post-init validation
- Serialization methods

### Async/Await
- Async context managers
- Concurrent processing with asyncio.gather
- Semaphore for concurrency control
- Proper exception handling

### Error Handling
- Custom exception classes
- Try-except-finally patterns
- Exception chaining
- Logging integration

### Documentation
- Google-style docstrings
- Module-level documentation
- Type hints as documentation
- Usage examples

## Files
- `data_processor.py` - Complete Python module with async processing

## Usage
```bash
python3 -m pip install asyncio

python3 data_processor.py
```

```python
from data_processor import DataProcessor, DataItem

# Create processor
processor = DataProcessor(timeout=5.0)

# Process single item
item = DataItem(id='1', value=42.0)
result = await processor.process_item(item)

# Process batch
results = await processor.process_batch(items, concurrency=10)
```

## Standards Demonstrated
- **Type hints:** All functions and classes fully typed
- **Dataclasses:** Structured data over dictionaries
- **Async:** Modern async/await patterns
- **Logging:** Structured logging throughout
- **Error handling:** Custom exceptions with context
- **Documentation:** Google-style docstrings
- **Naming:** snake_case for functions/variables, PascalCase for classes
