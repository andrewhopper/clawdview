# File UUID: 7b3d9e1f-2a4c-5d6e-8f0a-1b2c3d4e5f6a
#
# AWS provider configuration.
#

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  allowed_account_ids = [var.account]

  default_tags {
    tags = module.base.common_tags
  }
}
