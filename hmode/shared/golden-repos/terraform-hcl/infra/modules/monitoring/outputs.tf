# File UUID: 2c6d4e5f-6a7b-8c9d-e0f1-4c5d6e7f8a9b

output "alert_topic_arn" {
  description = "SNS topic ARN for alerts"
  value       = aws_sns_topic.alerts.arn
}

output "alert_topic_name" {
  description = "SNS topic name"
  value       = aws_sns_topic.alerts.name
}
