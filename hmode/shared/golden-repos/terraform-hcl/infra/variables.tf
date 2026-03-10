# File UUID: 4a2e8f91-3c7b-4d5e-9f1a-6b8c2d4e7f9a
#
# Variable definitions with validation.
# Mirrors the CDK config/schema.ts Zod schema.
#

# ============================================================================
# Core Settings
# ============================================================================

variable "context" {
  description = "Deployment context (e.g., work, personal, client-name)"
  type        = string

  validation {
    condition     = length(var.context) > 0
    error_message = "Context must not be empty."
  }
}

variable "stage" {
  description = "Deployment stage (e.g., dev, prod, blue, green, alpha)"
  type        = string

  validation {
    condition     = length(var.stage) > 0
    error_message = "Stage must not be empty."
  }
}

variable "account" {
  description = "AWS account ID"
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.account))
    error_message = "Account must be a 12-digit AWS account ID."
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project/application name"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.project_name))
    error_message = "Project name must be lowercase alphanumeric with hyphens."
  }
}

variable "stack_prefix" {
  description = "Resource name prefix (defaults to project_name)"
  type        = string
  default     = ""
}

# ============================================================================
# Domain Configuration
# ============================================================================

variable "domain" {
  description = "Domain configuration"
  type = object({
    root_domain     = string
    subdomain       = optional(string)
    hosted_zone_id  = optional(string)
    certificate_arn = optional(string)
  })
  default = null
}

# ============================================================================
# Notification Configuration
# ============================================================================

variable "notifications" {
  description = "Notification configuration"
  type = object({
    admin_email     = string
    support_email   = optional(string)
    alert_topic_arn = optional(string)
    ses_domain      = optional(string)
  })

  validation {
    condition     = can(regex("^[^@]+@[^@]+\\.[^@]+$", var.notifications.admin_email))
    error_message = "admin_email must be a valid email address."
  }
}

# ============================================================================
# Database Configuration
# ============================================================================

variable "database" {
  description = "Database configuration"
  type = object({
    instance_class       = optional(string, "t3.micro")
    allocated_storage    = optional(number, 20)
    multi_az             = optional(bool, false)
    deletion_protection  = optional(bool, false)
    backup_retention_days = optional(number, 7)
  })
  default = null
}

# ============================================================================
# Compute Configuration
# ============================================================================

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
  default = {}
}

# ============================================================================
# Monitoring Configuration
# ============================================================================

variable "monitoring" {
  description = "Monitoring configuration"
  type = object({
    enable_dashboards        = optional(bool, false)
    enable_tracing           = optional(bool, false)
    log_retention_days       = optional(number, 14)
    alarm_evaluation_periods = optional(number, 3)
  })
  default = {}
}

# ============================================================================
# Tags
# ============================================================================

variable "tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}
