# ===========================================
# Work Context - Development Stage
# ===========================================

# Core
context      = "work"
stage        = "dev"
account      = "123456789012"
region       = "us-east-1"
project_name = "my-app"
stack_prefix = "myapp"

# Domain
domain = {
  root_domain = "dev.example.com"
  subdomain   = "api"
}

# Notifications
notifications = {
  admin_email = "dev@example.com"
}

# Compute
compute = {
  lambda_memory  = 256
  lambda_timeout = 30
  task_cpu       = 256
  task_memory    = 512
  desired_count  = 1
  min_count      = 1
  max_count      = 2
}

# Monitoring
monitoring = {
  enable_dashboards        = false
  enable_tracing           = false
  log_retention_days       = 7
  alarm_evaluation_periods = 2
}

# Tags
tags = {
  Team       = "Platform"
  CostCenter = "Engineering"
}
