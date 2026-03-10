# File UUID: 1d5f2a3b-4c6e-7f8a-b092-3d4e5f6a7b8c
#
# Shared local values derived from variables.
#

locals {
  # Naming
  prefix = var.stack_prefix != "" ? var.stack_prefix : var.project_name
  resource_prefix = "${local.prefix}-${var.context}-${var.stage}"

  # Environment detection
  is_production = contains(["prod", "production", "green", "gamma"], lower(var.stage))

  # Full domain
  full_domain = var.domain != null ? (
    var.domain.subdomain != null
    ? "${var.domain.subdomain}.${var.domain.root_domain}"
    : var.domain.root_domain
  ) : null

  # Deployment identifier
  deploy_id = "${var.context}-${var.stage}"
}
