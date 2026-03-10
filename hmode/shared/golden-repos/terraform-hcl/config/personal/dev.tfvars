# ===========================================
# Personal Context - Development Stage
# ===========================================

# Core
context      = "personal"
stage        = "dev"
account      = "507745175693"
region       = "us-east-1"
project_name = "my-personal-project"
stack_prefix = "personal"

# Domain
domain = {
  root_domain = "dev.b.lfg.new"
  subdomain   = "api"
}

# Notifications
notifications = {
  admin_email = "andy@example.com"
}

# Database
database = {
  instance_class        = "t3.micro"
  allocated_storage     = 20
  multi_az              = false
  deletion_protection   = false
  backup_retention_days = 3
}

# Compute
compute = {
  lambda_memory  = 128
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
  enable_tracing           = false
  log_retention_days       = 3
  alarm_evaluation_periods = 2
}

# Tags
tags = {
  Owner   = "Andy"
  Context = "personal"
  Purpose = "Development"
}
