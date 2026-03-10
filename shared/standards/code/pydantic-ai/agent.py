"""
Pydantic AI Agent - Reference Example

Demonstrates:
- Agent creation and configuration
- Tool registration
- Dependency injection
- Structured outputs with validation
- Dynamic instructions
- Error handling

Reference: https://ai.pydantic.dev/
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import os

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


# Dependencies (injected into agent context)
@dataclass
class SupportDependencies:
    """Dependencies injected into agent context.

    Used for:
    - Database connections
    - API clients
    - Configuration
    - User context
    """
    customer_id: str
    customer_name: str
    database_url: str = "postgresql://localhost/support"


# Output models (structured responses)
class SupportOutput(BaseModel):
    """Structured output from support agent.

    Pydantic AI guarantees the response matches this schema.
    If validation fails, the agent automatically retries.
    """
    support_advice: str = Field(..., description="Advice to give to the customer")
    block_card: bool = Field(..., description="Whether to block the customer's card")
    risk_score: int = Field(..., ge=0, le=10, description="Risk score (0-10)")

    class Config:
        json_schema_extra = {
            "example": {
                "support_advice": "Your recent transaction appears legitimate. No action needed.",
                "block_card": False,
                "risk_score": 2
            }
        }


class CustomerInfo(BaseModel):
    """Customer information retrieved from database."""
    customer_id: str
    name: str
    account_balance: float
    account_status: str
    recent_transactions: List[str]


# Create agent with model and dependencies
support_agent = Agent(
    'openai:gpt-4o',  # Or any supported model
    deps_type=SupportDependencies,
    output_type=SupportOutput,
    system_prompt=(
        "You are a banking support agent helping customers with their accounts. "
        "Analyze the customer's situation and provide helpful advice. "
        "Consider blocking cards if there are suspicious activities."
    ),
)


# Register tools (functions the agent can call)
@support_agent.tool
async def get_customer_balance(
    ctx: RunContext[SupportDependencies],
) -> float:
    """Get the customer's current account balance.

    The docstring becomes the tool description sent to the LLM.

    Args:
        ctx: Agent context with injected dependencies

    Returns:
        Current account balance
    """
    # In real app, query database using ctx.deps.database_url
    customer_id = ctx.deps.customer_id

    # Mock data for example
    balances = {
        "customer_1": 5420.50,
        "customer_2": 120.00,
        "customer_3": 10500.75,
    }

    balance = balances.get(customer_id, 0.0)
    print(f"[Tool Called] get_customer_balance: ${balance}")
    return balance


@support_agent.tool
async def get_recent_transactions(
    ctx: RunContext[SupportDependencies],
    limit: int = 5,
) -> List[dict]:
    """Get the customer's recent transactions.

    Args:
        ctx: Agent context with dependencies
        limit: Maximum number of transactions to return

    Returns:
        List of recent transactions
    """
    customer_id = ctx.deps.customer_id

    # Mock transaction data
    transactions = {
        "customer_1": [
            {"date": "2024-01-15", "amount": -52.99, "merchant": "Amazon"},
            {"date": "2024-01-14", "amount": -15.00, "merchant": "Starbucks"},
            {"date": "2024-01-13", "amount": -89.99, "merchant": "Gas Station"},
            {"date": "2024-01-12", "amount": 2000.00, "merchant": "Payroll Deposit"},
            {"date": "2024-01-10", "amount": -125.50, "merchant": "Grocery Store"},
        ],
        "customer_2": [
            {"date": "2024-01-15", "amount": -1500.00, "merchant": "Unknown Merchant (Nigeria)"},
            {"date": "2024-01-15", "amount": -800.00, "merchant": "Wire Transfer International"},
        ],
        "customer_3": [
            {"date": "2024-01-15", "amount": -12.99, "merchant": "Netflix"},
            {"date": "2024-01-10", "amount": -45.00, "merchant": "Restaurant"},
        ],
    }

    customer_transactions = transactions.get(customer_id, [])[:limit]
    print(f"[Tool Called] get_recent_transactions: {len(customer_transactions)} transactions")
    return customer_transactions


@support_agent.tool
async def check_account_status(
    ctx: RunContext[SupportDependencies],
) -> str:
    """Check if the customer's account has any alerts or issues.

    Args:
        ctx: Agent context with dependencies

    Returns:
        Account status description
    """
    customer_id = ctx.deps.customer_id

    # Mock status data
    statuses = {
        "customer_1": "Active - No issues",
        "customer_2": "Active - Fraud alert triggered",
        "customer_3": "Active - No issues",
    }

    status = statuses.get(customer_id, "Unknown")
    print(f"[Tool Called] check_account_status: {status}")
    return status


# Dynamic instructions based on context
@support_agent.system_prompt
def dynamic_instructions(ctx: RunContext[SupportDependencies]) -> str:
    """Generate dynamic instructions based on customer context.

    This allows personalized guidance based on current context.

    Args:
        ctx: Agent context with dependencies

    Returns:
        Dynamic system instructions
    """
    customer_name = ctx.deps.customer_name
    return f"""
    You are assisting {customer_name}.

    Guidelines:
    - Be professional and empathetic
    - Always verify suspicious activity
    - Prioritize customer security
    - Explain your reasoning clearly
    """


# Example usage functions
async def handle_support_request(
    customer_id: str,
    customer_name: str,
    message: str,
) -> SupportOutput:
    """Handle a customer support request.

    Args:
        customer_id: Customer identifier
        customer_name: Customer name
        message: Customer's support request

    Returns:
        Structured support output
    """
    # Create dependencies
    deps = SupportDependencies(
        customer_id=customer_id,
        customer_name=customer_name,
        database_url="postgresql://localhost/support",
    )

    # Run agent with dependencies
    result = await support_agent.run(
        message,
        deps=deps,
    )

    # Result is guaranteed to be SupportOutput
    return result.data


async def example_normal_request():
    """Example: Normal customer inquiry."""
    print("\n=== Example 1: Normal Customer Inquiry ===")

    result = await handle_support_request(
        customer_id="customer_1",
        customer_name="Alice Johnson",
        message="Can you tell me my current account balance?",
    )

    print(f"\nAdvice: {result.support_advice}")
    print(f"Block Card: {result.block_card}")
    print(f"Risk Score: {result.risk_score}/10")


async def example_suspicious_activity():
    """Example: Suspicious activity detected."""
    print("\n=== Example 2: Suspicious Activity ===")

    result = await handle_support_request(
        customer_id="customer_2",
        customer_name="Bob Smith",
        message="I see charges on my account that I didn't make. There's a large international wire transfer.",
    )

    print(f"\nAdvice: {result.support_advice}")
    print(f"Block Card: {result.block_card}")
    print(f"Risk Score: {result.risk_score}/10")


async def example_account_review():
    """Example: General account review."""
    print("\n=== Example 3: Account Review ===")

    result = await handle_support_request(
        customer_id="customer_3",
        customer_name="Carol White",
        message="Can you review my account and let me know if everything looks normal?",
    )

    print(f"\nAdvice: {result.support_advice}")
    print(f"Block Card: {result.block_card}")
    print(f"Risk Score: {result.risk_score}/10")


# Advanced: Streaming responses
async def example_streaming():
    """Example: Stream agent responses."""
    print("\n=== Example 4: Streaming Response ===")

    deps = SupportDependencies(
        customer_id="customer_1",
        customer_name="Alice Johnson",
    )

    async with support_agent.run_stream(
        "Tell me about my recent transactions.",
        deps=deps,
    ) as result:
        # Stream text as it's generated
        print("\nStreaming response: ", end="", flush=True)
        async for text in result.stream_text():
            print(text, end="", flush=True)
        print()  # New line

        # Get final structured output
        output = await result.data()
        print(f"\nFinal output - Risk Score: {output.risk_score}/10")


# Advanced: Custom validation and retry
async def example_with_validation():
    """Example: Custom validation with retry."""
    print("\n=== Example 5: Custom Validation ===")

    # Create agent with custom validation
    class StrictSupportOutput(SupportOutput):
        """Extended output with additional validation."""

        @property
        def requires_supervisor(self) -> bool:
            """Check if supervisor escalation is needed."""
            return self.risk_score >= 7 or self.block_card

    # Override output type
    strict_agent = Agent(
        'openai:gpt-4o',
        deps_type=SupportDependencies,
        output_type=StrictSupportOutput,
    )

    # Copy tools from original agent
    strict_agent.tool(get_customer_balance)
    strict_agent.tool(get_recent_transactions)
    strict_agent.tool(check_account_status)

    deps = SupportDependencies(
        customer_id="customer_2",
        customer_name="Bob Smith",
    )

    result = await strict_agent.run(
        "I see unauthorized charges from Nigeria on my account!",
        deps=deps,
    )

    print(f"\nAdvice: {result.data.support_advice}")
    print(f"Requires Supervisor: {result.data.requires_supervisor}")


# Main execution
async def main():
    """Run all examples."""
    print("=" * 60)
    print("Pydantic AI Agent Examples")
    print("=" * 60)

    # Note: These examples require an OpenAI API key
    # Set OPENAI_API_KEY environment variable
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set. Examples will fail.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return

    await example_normal_request()
    await example_suspicious_activity()
    await example_account_review()

    # Uncomment to run streaming and validation examples
    # await example_streaming()
    # await example_with_validation()


if __name__ == "__main__":
    asyncio.run(main())
