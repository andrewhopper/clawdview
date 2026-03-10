# File UUID: 6c0d7e8f-9a1b-2c3d-e4f5-8c9d0e1f2a3b

output "resource_prefix" {
  description = "Resource naming prefix (prefix-context-stage)"
  value       = local.resource_prefix
}

output "is_production" {
  description = "Whether this is a production-like stage"
  value       = local.is_production
}

output "common_tags" {
  description = "Standard tags applied to all resources"
  value       = local.common_tags
}
