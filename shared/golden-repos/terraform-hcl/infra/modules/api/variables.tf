# File UUID: 8e2f0a1b-2c3d-4e5f-a6b7-0e1f2a3b4c5d

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

variable "compute" {
  description = "Compute configuration"
  type = object({
    lambda_memory  = optional(number, 256)
    lambda_timeout = optional(number, 30)
    task_cpu       = optional(number, 256)
    task_memory    = optional(number, 512)
    desired_count  = optional(number, 1)
    min_count      = optional(number, 1)
    max_count      = optional(number, 4)
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
