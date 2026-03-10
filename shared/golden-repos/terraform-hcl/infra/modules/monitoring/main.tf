# File UUID: 0a4b2c3d-4e5f-6a7b-c8d9-2a3b4c5d6e7f
#
# Monitoring module: SNS alerts + CloudWatch dashboard.
# Equivalent to CDK MonitoringStack.
#

# -----------------------------------------------------------------------------
# SNS Alert Topic
# -----------------------------------------------------------------------------

resource "aws_sns_topic" "alerts" {
  name         = "${var.resource_prefix}-alerts"
  display_name = "${var.project_name} Alerts (${var.stage})"

  tags = var.common_tags
}

resource "aws_sns_topic_subscription" "admin_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.notifications.admin_email
}

resource "aws_sns_topic_subscription" "support_email" {
  count     = var.notifications.support_email != null ? 1 : 0
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.notifications.support_email
}

# -----------------------------------------------------------------------------
# CloudWatch Dashboard (conditional)
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_dashboard" "main" {
  count          = var.monitoring.enable_dashboards ? 1 : 0
  dashboard_name = "${var.resource_prefix}-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "text"
        x      = 0
        y      = 0
        width  = 24
        height = 1
        properties = {
          markdown = "# ${var.project_name} - ${upper(var.stage)}"
        }
      }
    ]
  })
}
