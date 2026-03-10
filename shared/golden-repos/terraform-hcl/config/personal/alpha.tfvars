# ===========================================
# Personal Context - Alpha Stage
# ===========================================

# Core
context      = "personal"
stage        = "alpha"
account      = "507745175693"
region       = "us-east-1"
project_name = "my-personal-project"
stack_prefix = "personal"

# Domain
domain = {
  root_domain = "alpha.b.lfg.new"
  subdomain   = "api"
}

# Notifications
notifications = {
  admin_email = "andy@example.com"
}

# Compute
compute = {
  lambda_memory  = 256
  lambda_timeout = 15
  task_cpu       = 256
  task_memory    = 512
  desired_count  = 1
  min_count      = 1
  max_count      = 2
}

# Monitoring
monitoring = {
  enable_dashboards        = false
  enable_tracing           = true
  log_retention_days       = 7
  alarm_evaluation_periods = 3
}

# Tags
tags = {
  Owner   = "Andy"
  Context = "personal"
  Purpose = "Alpha Testing"
}
