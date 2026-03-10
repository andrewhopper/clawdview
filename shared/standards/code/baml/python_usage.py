"""
BAML Python Usage - Reference Example

Demonstrates:
- Calling BAML functions from Python
- Type-safe responses
- Error handling
- Async usage
- Integration patterns

Reference: https://docs.boundaryml.com/
"""

import asyncio
from typing import List

# Generated BAML client (after running `baml generate`)
# Import path depends on your project structure
from baml_client import b
from baml_client.types import (
    User,
    ProductReview,
    Sentiment,
    WeatherInfo,
    ValidatedProduct,
)


async def example_extract_user():
    """Example: Extract user information from text."""
    print("\n=== Example 1: Extract User ===")

    text = """
    My name is Alice Johnson, you can reach me at alice.johnson@email.com.
    I'm 28 years old and live in San Francisco.
    """

    # Call BAML function - type-safe!
    user = await b.ExtractUser(text)

    # Result is typed as User
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Age: {user.age}")

    return user


async def example_analyze_review():
    """Example: Analyze product review with structured output."""
    print("\n=== Example 2: Analyze Product Review ===")

    review_text = """
    I recently purchased the XYZ Laptop Pro and I'm thoroughly impressed!
    The build quality is exceptional, and the performance is blazing fast.
    The battery easily lasts a full workday. The display is stunning with
    great color accuracy.

    However, there are a few downsides. The laptop runs quite hot under load,
    and the fans can get pretty loud. Also, at $2,500, it's quite expensive.
    The port selection could be better - only 2 USB-C ports.

    Overall, I'd give it a solid 4 out of 5 stars. Great machine if you can
    afford it and don't mind the heat.
    """

    # Call BAML function
    review = await b.AnalyzeReview(review_text)

    # Structured, typed output
    print(f"Product: {review.product_name}")
    print(f"Rating: {review.rating}/5")
    print(f"Sentiment: {review.sentiment.value}")
    print(f"\nSummary: {review.summary}")

    print(f"\nPros ({len(review.pros)}):")
    for pro in review.pros:
        print(f"  + {pro}")

    print(f"\nCons ({len(review.cons)}):")
    for con in review.cons:
        print(f"  - {con}")

    return review


async def example_weather():
    """Example: Get weather with multiple parameters."""
    print("\n=== Example 3: Get Weather ===")

    weather = await b.GetWeather(
        city="Seattle",
        date="2024-01-20",
        units="Fahrenheit"
    )

    print(f"Weather for {weather.city}")
    print(f"Current: {weather.temperature}°F - {weather.conditions}")

    print(f"\n5-Day Forecast:")
    for day in weather.forecast:
        print(f"  {day.date}: {day.low_temp}°F - {day.high_temp}°F "
              f"(Rain: {day.precipitation_chance*100:.0f}%)")

    return weather


async def example_summarize():
    """Example: Summarize document with parameters."""
    print("\n=== Example 4: Summarize Document ===")

    document = """
    Artificial Intelligence has transformed the technology landscape in recent years.
    From natural language processing to computer vision, AI applications are now
    ubiquitous. Companies are leveraging machine learning to improve their products,
    automate processes, and gain insights from data. However, ethical considerations
    around AI deployment remain important. Issues like bias, privacy, and transparency
    need careful attention. As AI continues to advance, balancing innovation with
    responsibility will be crucial for the field's sustainable development.
    """

    # Call with different styles
    styles = ["technical", "casual", "executive"]

    for style in styles:
        summary = await b.SummarizeDocument(
            document=document,
            max_length=50,
            style=style
        )
        print(f"\n{style.title()} style:")
        print(f"  {summary}")


async def example_classify():
    """Example: Classify text into categories."""
    print("\n=== Example 5: Classify Text ===")

    texts = [
        "The company's revenue grew 25% this quarter",
        "New CPU architecture delivers 40% better performance",
        "Scientists discover new exoplanet in habitable zone",
        "Local team wins championship in overtime thriller",
    ]

    categories = ["Business", "Technology", "Science", "Sports", "Entertainment"]

    for text in texts:
        category = await b.ClassifyText(
            text=text,
            categories=categories
        )
        print(f"\nText: {text}")
        print(f"Category: {category}")


async def example_extract_keywords():
    """Example: Extract keywords from text."""
    print("\n=== Example 6: Extract Keywords ===")

    text = """
    Cloud computing has revolutionized how businesses operate. With services like
    AWS, Azure, and Google Cloud, companies can scale their infrastructure instantly.
    Containerization with Docker and Kubernetes has made deployment easier.
    Serverless computing is gaining popularity for its cost-effectiveness and scalability.
    """

    keywords = await b.ExtractKeywords(text, max_keywords=10)

    print("Extracted Keywords:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")


async def example_validated_product():
    """Example: Extract with validation constraints."""
    print("\n=== Example 7: Validated Product Extraction ===")

    text = """
    The SuperWidget 3000 is now available for $149.99.
    We have 50 units in stock. Customer rating: 4.5 stars.
    """

    try:
        product = await b.ExtractProductInfo(text)

        print(f"Product: {product.name}")
        print(f"Price: ${product.price:.2f}")
        print(f"Stock: {product.stock} units")
        print(f"Rating: {product.rating}/5.0")

    except Exception as e:
        print(f"Validation failed: {e}")


async def example_error_handling():
    """Example: Error handling patterns."""
    print("\n=== Example 8: Error Handling ===")

    # BAML handles many errors automatically:
    # - Malformed JSON (retries with reflection)
    # - Type validation errors (retries with error message)
    # - LLM API errors (exponential backoff retry)

    try:
        # This might fail if constraints aren't met
        product = await b.ExtractProductInfo("Invalid product data")
        print("Success!")

    except ValueError as e:
        print(f"Validation error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


async def example_batch_processing():
    """Example: Process multiple items efficiently."""
    print("\n=== Example 9: Batch Processing ===")

    texts = [
        "John Smith, john@example.com, age 30",
        "Jane Doe, jane@example.com, age 25",
        "Bob Wilson, bob@example.com, age 45",
    ]

    # Process in parallel
    tasks = [b.ExtractUser(text) for text in texts]
    users = await asyncio.gather(*tasks)

    print("Extracted users:")
    for user in users:
        print(f"  - {user.name} ({user.age}): {user.email}")


# Integration patterns
class BAMLService:
    """Service wrapper for BAML functions.

    Demonstrates:
    - Caching
    - Rate limiting
    - Error recovery
    - Logging
    """

    def __init__(self):
        self.cache = {}

    async def analyze_review_cached(self, review_text: str) -> ProductReview:
        """Analyze review with caching."""
        # Check cache
        cache_key = hash(review_text)
        if cache_key in self.cache:
            print("[Cache hit]")
            return self.cache[cache_key]

        # Call BAML function
        print("[Cache miss - calling LLM]")
        result = await b.AnalyzeReview(review_text)

        # Store in cache
        self.cache[cache_key] = result

        return result

    async def extract_user_with_retry(
        self,
        text: str,
        max_retries: int = 3
    ) -> User:
        """Extract user with custom retry logic."""
        for attempt in range(max_retries):
            try:
                return await b.ExtractUser(text)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(2 ** attempt)


async def main():
    """Run all examples."""
    print("=" * 60)
    print("BAML Python Usage Examples")
    print("=" * 60)

    # Note: Requires BAML project setup and API keys
    print("\n⚠️  Prerequisites:")
    print("1. Run 'baml generate' to generate Python client")
    print("2. Set LLM API keys (OPENAI_API_KEY, etc.)")
    print("3. Ensure baml_client is in Python path")

    try:
        await example_extract_user()
        await example_analyze_review()
        # await example_weather()
        # await example_summarize()
        # await example_classify()
        # await example_extract_keywords()
        # await example_validated_product()
        # await example_error_handling()
        # await example_batch_processing()

        # Service pattern example
        # service = BAMLService()
        # review = await service.analyze_review_cached("Great product!")

    except ImportError:
        print("\n❌ Error: baml_client not found")
        print("Run 'baml generate' in your BAML project directory")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
