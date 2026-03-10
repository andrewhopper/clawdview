// BAML (Boundary Markup Language) - Reference Example
//
// Demonstrates:
// - Type definitions
// - Function definitions
// - Structured outputs
// - LLM client configuration
// - Prompts and templates
//
// Reference: https://docs.boundaryml.com/

// ============================================================================
// Type Definitions
// ============================================================================

// Basic class with typed fields
class User {
  name string @description("User's full name")
  email string @description("User's email address")
  age int @description("User's age in years")
}

// Enum for constrained values
enum Sentiment {
  POSITIVE
  NEGATIVE
  NEUTRAL
}

// Class with nested types
class ProductReview {
  product_name string @description("Name of the product")
  rating int @description("Rating from 1-5") @assert(this >= 1 and this <= 5)
  sentiment Sentiment @description("Overall sentiment")
  summary string @description("Brief summary of the review")
  pros string[] @description("List of positive aspects")
  cons string[] @description("List of negative aspects")
}

// Complex nested structure
class WeatherInfo {
  city string @description("City name")
  temperature float @description("Temperature in Fahrenheit")
  conditions string @description("Weather conditions description")
  forecast DailyForecast[] @description("5-day forecast")
}

class DailyForecast {
  date string @description("Date in YYYY-MM-DD format")
  high_temp float @description("High temperature")
  low_temp float @description("Low temperature")
  precipitation_chance float @description("Chance of rain (0-1)")
}

// Optional fields
class UserProfile {
  username string @description("Username (required)")
  full_name string? @description("Full name (optional)")
  bio string? @description("User biography (optional)")
  verified bool @description("Whether user is verified")
}

// Union types (one of multiple types)
class APIResponse {
  status string @description("Response status")
  data User | ProductReview @description("Response data")
}


// ============================================================================
// Client Configurations
// ============================================================================

// OpenAI client
client<llm> GPT4 {
  provider openai
  options {
    model gpt-4o
    temperature 0.7
    max_tokens 1000
  }
}

// Anthropic client
client<llm> Claude {
  provider anthropic
  options {
    model claude-3-5-sonnet-20241022
    temperature 0.5
    max_tokens 2000
  }
}

// Multiple clients with fallback
client<llm> Production {
  provider openai
  options {
    model gpt-4o
    temperature 0.7
  }
  retry_policy {
    max_retries 3
    strategy exponential_backoff
  }
}


// ============================================================================
// Function Definitions
// ============================================================================

// Simple extraction function
function ExtractUser(text: string) -> User {
  client GPT4

  prompt #"
    Extract user information from the following text:

    {{ text }}

    Return the user's name, email, and age.
  "#
}

// Function with structured output
function AnalyzeReview(review_text: string) -> ProductReview {
  client GPT4

  prompt #"
    Analyze the following product review and extract structured information:

    Review:
    {{ review_text }}

    Extract:
    - Product name
    - Rating (1-5)
    - Sentiment (POSITIVE, NEGATIVE, or NEUTRAL)
    - Brief summary
    - List of pros (positive aspects)
    - List of cons (negative aspects)
  "#
}

// Function with multiple inputs
function GetWeather(
  city: string,
  date: string,
  units: string
) -> WeatherInfo {
  client GPT4

  prompt #"
    Get weather information for {{ city }} on {{ date }}.
    Return temperatures in {{ units }}.

    Provide current conditions and a 5-day forecast.
  "#
}

// Function with complex logic
function SummarizeDocument(
  document: string,
  max_length: int,
  style: string
) -> string {
  client Claude

  prompt #"
    Summarize the following document in {{ style }} style.
    Keep the summary under {{ max_length }} words.

    Document:
    {{ document }}

    Summary:
  "#
}

// Function with conditional logic
function ClassifyText(text: string, categories: string[]) -> string {
  client GPT4

  prompt #"
    Classify the following text into one of these categories:

    {% for category in categories %}
    - {{ category }}
    {% endfor %}

    Text: {{ text }}

    Return only the category name.
  "#
}

// Function returning list
function ExtractKeywords(text: string, max_keywords: int) -> string[] {
  client GPT4

  prompt #"
    Extract the top {{ max_keywords }} keywords from this text:

    {{ text }}

    Return only the keywords, one per line.
  "#
}

// Function with system prompt
function ChatAgent(user_message: string, conversation_history: string[]) -> string {
  client GPT4

  prompt #"
    You are a helpful AI assistant.

    Previous conversation:
    {% for message in conversation_history %}
    {{ message }}
    {% endfor %}

    User: {{ user_message }}

    Assistant:
  "#
}


// ============================================================================
// Advanced: Tests and Examples
// ============================================================================

// Test cases (run in BAML Playground)
test TestExtractUser {
  functions [ExtractUser]

  args {
    text "My name is John Doe, email john@example.com, I'm 30 years old"
  }
}

test TestAnalyzeReview {
  functions [AnalyzeReview]

  args {
    review_text """
      This laptop is amazing! The battery life is incredible, lasting over 12 hours.
      The screen is bright and crisp. However, it's a bit heavy to carry around,
      and the price is quite steep. Overall, I'd rate it 4 out of 5 stars.
    """
  }
}

test TestWeather {
  functions [GetWeather]

  args {
    city "San Francisco"
    date "2024-01-15"
    units "Fahrenheit"
  }
}


// ============================================================================
// Advanced: Validation and Constraints
// ============================================================================

class ValidatedProduct {
  name string @assert(this.length > 0) @description("Product name (non-empty)")
  price float @assert(this > 0) @description("Price (must be positive)")
  stock int @assert(this >= 0) @description("Stock quantity (non-negative)")
  rating float @assert(this >= 1.0 and this <= 5.0) @description("Rating (1-5)")
}

function ExtractProductInfo(text: string) -> ValidatedProduct {
  client GPT4

  prompt #"
    Extract product information from:
    {{ text }}

    Ensure all constraints are met:
    - Name must not be empty
    - Price must be positive
    - Stock must be non-negative
    - Rating must be between 1.0 and 5.0
  "#
}


// ============================================================================
// Advanced: Error Handling
// ============================================================================

// BAML handles:
// - JSON parsing errors (auto-retry with reflection)
// - Type validation errors (auto-retry with error message)
// - LLM API errors (retry with exponential backoff)
// - Network errors (configurable retry policy)

// You can configure retry behavior:
client<llm> RobustClient {
  provider openai
  options {
    model gpt-4o
  }
  retry_policy {
    max_retries 5
    strategy exponential_backoff
    initial_delay_ms 1000
    max_delay_ms 30000
  }
}
