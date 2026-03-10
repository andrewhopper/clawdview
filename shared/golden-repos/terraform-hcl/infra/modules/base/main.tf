# File UUID: 4a8b5c6d-7e9f-0a1b-c2d3-6a7b8c9d0e1f
#
# Base module: common naming, tags, and environment detection.
# Equivalent to CDK BaseStack construct.
#

locals {
  prefix          = var.stack_prefix != "" ? var.stack_prefix : var.project_name
  resource_prefix = "${local.prefix}-${var.context}-${var.stage}"

  is_production = contains(
    ["prod", "production", "green", "gamma"],
    lower(var.stage)
  )

  common_tags = merge(
    {
      Project   = var.project_name
      Context   = var.context
      Stage     = var.stage
      ManagedBy = "Terraform"
    },
    var.tags
  )
}
