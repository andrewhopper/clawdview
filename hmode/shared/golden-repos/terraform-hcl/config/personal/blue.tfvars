# ===========================================
# Personal Context - Blue Stage (Production A)
# ===========================================

# Core
context      = "personal"
stage        = "blue"
account      = "507745175693"
region       = "us-east-1"
project_name = "my-personal-project"
stack_prefix = "personal"

# Domain
domain = {
  root_domain = "b.lfg.new"
  subdomain   = "api"
}

# Notifications
notifications = {
  admin_email = "andy@example.com"
}

# Compute
compute = {
  lambda_memory  = 512
  lambda_timeout = 30
  task_cpu       = 512
  task_memory    = 1024
  desired_count  = 2
  min_count      = 1
  max_count      = 4
}

# Monitoring
monitoring = {
  enable_dashboards        = true
  enable_tracing           = true
  log_retention_days       = 30
  alarm_evaluation_periods = 3
}

# Tags
tags = {
  Owner   = "Andy"
  Context = "personal"
  Purpose = "Production-Blue"
}
