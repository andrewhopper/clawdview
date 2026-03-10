# File UUID: 5b9c6d7e-8f0a-1b2c-d3e4-7b8c9d0e1f2a

variable "project_name" {
  description = "Project/application name"
  type        = string
}

variable "context" {
  description = "Deployment context"
  type        = string
}

variable "stage" {
  description = "Deployment stage"
  type        = string
}

variable "stack_prefix" {
  description = "Resource name prefix (defaults to project_name)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}
