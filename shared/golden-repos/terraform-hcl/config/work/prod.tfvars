# ===========================================
# Work Context - Production Stage
# ===========================================

# Core
context      = "work"
stage        = "prod"
account      = "123456789012"
region       = "us-east-1"
project_name = "my-app"
stack_prefix = "myapp"

# Domain
domain = {
  root_domain = "example.com"
  subdomain   = "api"
  # hosted_zone_id  = "Z1234567890ABC"
  # certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/..."
}

# Notifications
notifications = {
  admin_email   = "ops@example.com"
  support_email = "support@example.com"
  ses_domain    = "example.com"
}

# Database
database = {
  instance_class        = "r5.large"
  allocated_storage     = 100
  multi_az              = true
  deletion_protection   = true
  backup_retention_days = 30
}

# Compute
compute = {
  lambda_memory  = 1024
  lambda_timeout = 30
  task_cpu       = 1024
  task_memory    = 2048
  desired_count  = 3
  min_count      = 2
  max_count      = 10
}

# Monitoring
monitoring = {
  enable_dashboards        = true
  enable_tracing           = true
  log_retention_days       = 90
  alarm_evaluation_periods = 5
}

# Tags
tags = {
  Team       = "Platform"
  CostCenter = "Engineering"
  Compliance = "SOC2"
}
