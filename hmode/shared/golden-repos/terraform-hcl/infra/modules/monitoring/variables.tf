# File UUID: 1b5c3d4e-5f6a-7b8c-d9e0-3b4c5d6e7f8a

variable "resource_prefix" {
  description = "Resource naming prefix from base module"
  type        = string
}

variable "common_tags" {
  description = "Common tags from base module"
  type        = map(string)
}

variable "is_production" {
  description = "Whether this is a production deployment"
  type        = bool
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "stage" {
  description = "Deployment stage"
  type        = string
}

variable "notifications" {
  description = "Notification configuration"
  type = object({
    admin_email     = string
    support_email   = optional(string)
    alert_topic_arn = optional(string)
    ses_domain      = optional(string)
  })
}

variable "monitoring" {
  description = "Monitoring configuration"
  type = object({
    enable_dashboards        = optional(bool, false)
    enable_tracing           = optional(bool, false)
    log_retention_days       = optional(number, 14)
    alarm_evaluation_periods = optional(number, 3)
  })
}
