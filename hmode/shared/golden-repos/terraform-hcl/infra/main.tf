# File UUID: 2e6a3b4c-5d7f-8a9b-c0d1-4e5f6a7b8c9d
#
# Root module: composes all infrastructure modules.
#
# Usage:
#   CONTEXT=work STAGE=dev make infra-deploy
#

# -----------------------------------------------------------------------------
# Base module (common tags, naming, environment detection)
# -----------------------------------------------------------------------------

module "base" {
  source = "./modules/base"

  project_name = var.project_name
  context      = var.context
  stage        = var.stage
  stack_prefix = var.stack_prefix
  tags         = var.tags
}

# -----------------------------------------------------------------------------
# Monitoring module (SNS alerts, CloudWatch dashboard)
# Deploy first — other modules may reference the alert topic.
# -----------------------------------------------------------------------------

module "monitoring" {
  source = "./modules/monitoring"

  resource_prefix = module.base.resource_prefix
  common_tags     = module.base.common_tags
  is_production   = module.base.is_production
  project_name    = var.project_name
  stage           = var.stage
  notifications   = var.notifications
  monitoring      = var.monitoring
}

# -----------------------------------------------------------------------------
# API module (Lambda + API Gateway)
# -----------------------------------------------------------------------------

module "api" {
  source = "./modules/api"

  resource_prefix = module.base.resource_prefix
  common_tags     = module.base.common_tags
  is_production   = module.base.is_production
  project_name    = var.project_name
  stage           = var.stage
  compute         = var.compute
  monitoring      = var.monitoring
}
