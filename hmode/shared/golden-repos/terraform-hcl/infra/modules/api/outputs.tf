# File UUID: 9f3a1b2c-3d4e-5f6a-b7c8-1f2a3b4c5d6e

output "api_url" {
  description = "API Gateway invoke URL"
  value       = aws_apigatewayv2_api.api.api_endpoint
}

output "api_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.api.id
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.handler.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.handler.arn
}
