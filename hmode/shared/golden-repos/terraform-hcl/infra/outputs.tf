# File UUID: 3f7b4c5d-6e8a-9b0c-d1e2-5f6a7b8c9d0e
#
# Root outputs.
#

output "deploy_id" {
  description = "Deployment identifier (context-stage)"
  value       = local.deploy_id
}

output "resource_prefix" {
  description = "Resource naming prefix"
  value       = module.base.resource_prefix
}

output "is_production" {
  description = "Whether this is a production deployment"
  value       = module.base.is_production
}

# Monitoring outputs
output "alert_topic_arn" {
  description = "SNS topic ARN for alerts"
  value       = module.monitoring.alert_topic_arn
}

# API outputs
output "api_url" {
  description = "API Gateway invoke URL"
  value       = module.api.api_url
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = module.api.lambda_function_name
}
