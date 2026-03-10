# File UUID: 9c4e0f2a-3b5d-6e7f-a081-2c3d4e5f6a7b
#
# Remote state backend (S3 + DynamoDB).
#
# USAGE:
#   terraform init \
#     -backend-config="bucket=my-project-tfstate" \
#     -backend-config="key=work/dev/terraform.tfstate" \
#     -backend-config="region=us-east-1" \
#     -backend-config="dynamodb_table=my-project-tflock"
#
# The Makefile handles this automatically using CONTEXT and STAGE variables.
#

terraform {
  backend "s3" {
    # Values injected via -backend-config in Makefile.
    # bucket         = "PROJECT-tfstate"
    # key            = "CONTEXT/STAGE/terraform.tfstate"
    # region         = "us-east-1"
    # dynamodb_table = "PROJECT-tflock"
    encrypt = true
  }
}
