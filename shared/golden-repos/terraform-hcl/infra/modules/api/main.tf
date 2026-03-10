# File UUID: 7d1e8f0a-1b2c-3d4e-f5a6-9d0e1f2a3b4c
#
# API module: Lambda + API Gateway.
# Equivalent to CDK ApiStack.
#

# -----------------------------------------------------------------------------
# Lambda Function
# -----------------------------------------------------------------------------

data "archive_file" "handler" {
  type        = "zip"
  output_path = "${path.module}/handler.zip"

  source {
    content  = <<-JS
      exports.handler = async (event) => {
        return {
          statusCode: 200,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: "Hello from ${var.stage}!" }),
        };
      };
    JS
    filename = "index.js"
  }
}

resource "aws_cloudwatch_log_group" "handler" {
  name              = "/aws/lambda/${var.resource_prefix}-api-handler"
  retention_in_days = var.monitoring.log_retention_days

  tags = var.common_tags
}

resource "aws_iam_role" "handler" {
  name = "${var.resource_prefix}-api-handler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "handler_basic" {
  role       = aws_iam_role.handler.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "handler_xray" {
  count      = var.monitoring.enable_tracing ? 1 : 0
  role       = aws_iam_role.handler.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

resource "aws_lambda_function" "handler" {
  function_name = "${var.resource_prefix}-api-handler"
  role          = aws_iam_role.handler.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"

  filename         = data.archive_file.handler.output_path
  source_code_hash = data.archive_file.handler.output_base64sha256

  memory_size = var.compute.lambda_memory
  timeout     = var.compute.lambda_timeout

  tracing_config {
    mode = var.monitoring.enable_tracing ? "Active" : "PassThrough"
  }

  environment {
    variables = {
      ENV          = var.stage
      PROJECT_NAME = var.project_name
    }
  }

  depends_on = [aws_cloudwatch_log_group.handler]

  tags = var.common_tags
}

# -----------------------------------------------------------------------------
# API Gateway
# -----------------------------------------------------------------------------

resource "aws_apigatewayv2_api" "api" {
  name          = "${var.resource_prefix}-api"
  protocol_type = "HTTP"
  description   = "${var.project_name} API (${var.stage})"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }

  tags = var.common_tags
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      integrationError = "$context.integrationErrorMessage"
    })
  }

  tags = var.common_tags
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/apigateway/${var.resource_prefix}-api"
  retention_in_days = var.monitoring.log_retention_days

  tags = var.common_tags
}

resource "aws_apigatewayv2_integration" "handler" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.handler.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.handler.id}"
}

resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.handler.id}"
}

resource "aws_lambda_permission" "api" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
