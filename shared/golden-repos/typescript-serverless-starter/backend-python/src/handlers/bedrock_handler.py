"""
Bedrock AI Handler with Lambda Powertools, X-Ray, and Pydantic validation.
"""

import json
import os
from typing import Any

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field

from lib.secrets import get_secret
from models.requests import ChatRequest, ChatResponse, EmbeddingRequest, EmbeddingResponse

# Initialize Powertools
logger = Logger(service="bedrock-handler")
tracer = Tracer(service="bedrock-handler")
metrics = Metrics(namespace="ServerlessStarter", service="bedrock-handler")

app = APIGatewayRestResolver(enable_validation=True)

# Environment variables
SECRETS_ARN = os.environ.get("SECRETS_ARN", "")
TABLE_NAME = os.environ.get("TABLE_NAME", "")


@tracer.capture_method
def get_bedrock_client():
    """Get Bedrock Runtime client with X-Ray tracing."""
    from aws_xray_sdk.core import patch_all
    patch_all()

    return boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )


@app.get("/ai/health")
@tracer.capture_method
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bedrock-handler"}


@app.post("/ai/chat")
@tracer.capture_method
@metrics.log_metrics(capture_cold_start_metric=True)
def chat_completion(request: ChatRequest) -> ChatResponse:
    """
    Chat completion using AWS Bedrock Claude model.

    Retrieves API configuration from Secrets Manager.
    """
    logger.info("Processing chat request", extra={"model": request.model})
    metrics.add_metric(name="ChatRequests", unit=MetricUnit.Count, value=1)

    try:
        # Get secrets if needed for custom configuration
        secrets = get_secret(SECRETS_ARN) if SECRETS_ARN else {}

        bedrock = get_bedrock_client()

        # Prepare messages for Claude
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        # Call Bedrock
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": messages,
        }

        if request.system:
            body["system"] = request.system

        response = bedrock.invoke_model(
            modelId=request.model,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        result = json.loads(response["body"].read())

        # Extract response
        content = result.get("content", [{}])[0].get("text", "")
        usage = result.get("usage", {})

        metrics.add_metric(
            name="InputTokens",
            unit=MetricUnit.Count,
            value=usage.get("input_tokens", 0)
        )
        metrics.add_metric(
            name="OutputTokens",
            unit=MetricUnit.Count,
            value=usage.get("output_tokens", 0)
        )

        logger.info("Chat completion successful", extra={
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens")
        })

        return ChatResponse(
            content=content,
            model=request.model,
            usage={
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
            },
            stop_reason=result.get("stop_reason", "end_turn")
        )

    except Exception as e:
        logger.exception("Error processing chat request")
        metrics.add_metric(name="ChatErrors", unit=MetricUnit.Count, value=1)
        raise


@app.post("/ai/embeddings")
@tracer.capture_method
@metrics.log_metrics(capture_cold_start_metric=True)
def create_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generate embeddings using AWS Bedrock Titan model.
    """
    logger.info("Processing embedding request", extra={
        "model": request.model,
        "text_count": len(request.texts)
    })
    metrics.add_metric(name="EmbeddingRequests", unit=MetricUnit.Count, value=1)

    try:
        bedrock = get_bedrock_client()
        embeddings = []

        for text in request.texts:
            body = {
                "inputText": text,
            }

            response = bedrock.invoke_model(
                modelId=request.model,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )

            result = json.loads(response["body"].read())
            embeddings.append(result.get("embedding", []))

        logger.info("Embeddings generated successfully", extra={
            "count": len(embeddings),
            "dimensions": len(embeddings[0]) if embeddings else 0
        })

        return EmbeddingResponse(
            embeddings=embeddings,
            model=request.model,
            dimensions=len(embeddings[0]) if embeddings else 0
        )

    except Exception as e:
        logger.exception("Error generating embeddings")
        metrics.add_metric(name="EmbeddingErrors", unit=MetricUnit.Count, value=1)
        raise


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    """Main Lambda handler."""
    return app.resolve(event, context)
