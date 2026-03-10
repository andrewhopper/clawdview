# File UUID: 3d7e4f5a-6b8c-9d0e-f1a2-5e6f7a8b9c0d
#
# Terraform HCL - Multi-Context/Multi-Stage Deployment
# Mirrors the CDK golden repo Makefile targets exactly.
#

.PHONY: init validate plan apply fmt lint
.PHONY: infra-bootstrap infra-deploy infra-destroy infra-diff infra-rollback
.PHONY: infra-status infra-outputs infra-list
.PHONY: secrets-load secrets-store help

# ============================================================================
# Configuration
# ============================================================================

TIMESTAMP := $(shell date +%Y%m%d-%H%M)
CONTEXT ?= work
STAGE ?= dev
DEPLOY_ID := $(CONTEXT)-$(STAGE)
RELEASES_DIR := infra/deploys/$(DEPLOY_ID)/releases
RELEASE_DIR := $(RELEASES_DIR)/$(TIMESTAMP)
CURRENT_LINK := infra/deploys/$(DEPLOY_ID)/current
SHARED_DIR := infra/deploys/$(DEPLOY_ID)/shared
KEEP_RELEASES := 5
AWS_PROFILE ?= admin-507745175693
AWS_REGION ?= us-east-1

# Terraform vars
TF_DIR := infra
TF_VARS := -var-file=../config/$(CONTEXT)/$(STAGE).tfvars
TF_BACKEND_KEY := $(CONTEXT)/$(STAGE)/terraform.tfstate

# State bucket (override per project)
TF_STATE_BUCKET ?= $(shell echo $(PROJECT_NAME)-tfstate 2>/dev/null || echo "my-project-tfstate")
TF_LOCK_TABLE ?= $(shell echo $(PROJECT_NAME)-tflock 2>/dev/null || echo "my-project-tflock")

# ============================================================================
# Development Commands
# ============================================================================

init:
	cd $(TF_DIR) && terraform init -upgrade

validate:
	cd $(TF_DIR) && terraform validate

plan:
	cd $(TF_DIR) && terraform plan $(TF_VARS)

apply:
	cd $(TF_DIR) && terraform apply $(TF_VARS)

fmt:
	terraform fmt -recursive $(TF_DIR)

lint:
	@command -v tflint >/dev/null 2>&1 && tflint --init && tflint $(TF_DIR) || echo "tflint not installed, skipping"

check: validate fmt lint

clean:
	rm -rf $(TF_DIR)/.terraform $(TF_DIR)/.terraform.lock.hcl

# ============================================================================
# Capistrano-style Deployment Management
# ============================================================================

infra-bootstrap:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Bootstrapping Terraform"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "   State Bucket: $(TF_STATE_BUCKET)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@mkdir -p $(RELEASE_DIR) $(SHARED_DIR)
	@# Create S3 state bucket if it doesn't exist
	@aws s3api head-bucket --bucket $(TF_STATE_BUCKET) --profile $(AWS_PROFILE) --region $(AWS_REGION) 2>/dev/null || \
		(echo "Creating state bucket: $(TF_STATE_BUCKET)" && \
		aws s3api create-bucket --bucket $(TF_STATE_BUCKET) --profile $(AWS_PROFILE) --region $(AWS_REGION) && \
		aws s3api put-bucket-versioning --bucket $(TF_STATE_BUCKET) --versioning-configuration Status=Enabled --profile $(AWS_PROFILE) --region $(AWS_REGION) && \
		aws s3api put-bucket-encryption --bucket $(TF_STATE_BUCKET) --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}' --profile $(AWS_PROFILE) --region $(AWS_REGION) && \
		aws s3api put-public-access-block --bucket $(TF_STATE_BUCKET) --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true --profile $(AWS_PROFILE) --region $(AWS_REGION))
	@# Create DynamoDB lock table if it doesn't exist
	@aws dynamodb describe-table --table-name $(TF_LOCK_TABLE) --profile $(AWS_PROFILE) --region $(AWS_REGION) 2>/dev/null || \
		(echo "Creating lock table: $(TF_LOCK_TABLE)" && \
		aws dynamodb create-table --table-name $(TF_LOCK_TABLE) \
			--attribute-definitions AttributeName=LockID,AttributeType=S \
			--key-schema AttributeName=LockID,KeyType=HASH \
			--billing-mode PAY_PER_REQUEST \
			--profile $(AWS_PROFILE) --region $(AWS_REGION))
	@# Init Terraform with backend config
	cd $(TF_DIR) && terraform init -upgrade \
		-backend-config="bucket=$(TF_STATE_BUCKET)" \
		-backend-config="key=$(TF_BACKEND_KEY)" \
		-backend-config="region=$(AWS_REGION)" \
		-backend-config="dynamodb_table=$(TF_LOCK_TABLE)" \
		-backend-config="encrypt=true" \
		2>&1 | tee ../$(RELEASE_DIR)/bootstrap.log
	@echo "✓ Bootstrap complete for $(DEPLOY_ID)"

infra-deploy:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Deploying Infrastructure"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "   Deploy ID: $(DEPLOY_ID)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@mkdir -p $(RELEASE_DIR) $(SHARED_DIR)
	@# Load secrets before deploy
	@if [ -f config/$(CONTEXT)/load-secrets.sh ]; then \
		echo "🔑 Loading secrets from AWS Secrets Manager..."; \
		. config/$(CONTEXT)/load-secrets.sh; \
	fi
	@# Re-init for correct backend key
	cd $(TF_DIR) && terraform init -reconfigure \
		-backend-config="bucket=$(TF_STATE_BUCKET)" \
		-backend-config="key=$(TF_BACKEND_KEY)" \
		-backend-config="region=$(AWS_REGION)" \
		-backend-config="dynamodb_table=$(TF_LOCK_TABLE)" \
		-backend-config="encrypt=true" \
		> /dev/null 2>&1
	@# Plan
	cd $(TF_DIR) && terraform plan $(TF_VARS) -out=tfplan 2>&1 | tee ../$(RELEASE_DIR)/plan.log
	@# Apply
	cd $(TF_DIR) && terraform apply -auto-approve tfplan 2>&1 | tee ../$(RELEASE_DIR)/deploy.log
	@# Capture outputs
	cd $(TF_DIR) && terraform output -json > ../$(RELEASE_DIR)/outputs.json 2>/dev/null || echo '{}' > $(RELEASE_DIR)/outputs.json
	@# Clean up plan file
	@rm -f $(TF_DIR)/tfplan
	@# Update symlink
	@ln -sfn releases/$(TIMESTAMP) $(CURRENT_LINK)
	@# Write manifest
	@echo '{"timestamp":"$(TIMESTAMP)","context":"$(CONTEXT)","stage":"$(STAGE)","status":"deployed","git_commit":"$(shell git rev-parse HEAD 2>/dev/null || echo unknown)","iac":"terraform"}' > $(RELEASE_DIR)/manifest.json
	@echo ""
	@echo "✓ Deployed: $(RELEASE_DIR)"
	@echo "✓ Current symlink updated: $(CURRENT_LINK)"
	@# Cleanup old releases (keep last N)
	@cd $(RELEASES_DIR) 2>/dev/null && ls -t | tail -n +$$(($(KEEP_RELEASES)+1)) | xargs rm -rf 2>/dev/null || true

infra-rollback:
	@echo "📋 Available releases for $(DEPLOY_ID):"
	@ls -t $(RELEASES_DIR) 2>/dev/null | head -$(KEEP_RELEASES) || echo "No releases found"
	@echo ""
	@echo "Usage: make infra-rollback CONTEXT=$(CONTEXT) STAGE=$(STAGE) RELEASE=YYYYMMDD-HHMM"
ifdef RELEASE
	@if [ -d "$(RELEASES_DIR)/$(RELEASE)" ]; then \
		ln -sfn releases/$(RELEASE) $(CURRENT_LINK); \
		echo "✓ Rolled back $(DEPLOY_ID) to $(RELEASE)"; \
		echo "⚠️  Note: This updates the symlink. Re-apply from that state if needed."; \
	else \
		echo "✗ Release $(RELEASE) not found"; \
		exit 1; \
	fi
endif

infra-destroy:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🗑️  Destroying Infrastructure"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@mkdir -p $(RELEASE_DIR)
	cd $(TF_DIR) && terraform destroy $(TF_VARS) -auto-approve 2>&1 | tee ../$(RELEASE_DIR)/destroy.log
	@echo '{"timestamp":"$(TIMESTAMP)","context":"$(CONTEXT)","stage":"$(STAGE)","status":"destroyed","iac":"terraform"}' > $(RELEASE_DIR)/manifest.json

infra-diff:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔍 Infrastructure Diff"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd $(TF_DIR) && terraform plan $(TF_VARS)

# ============================================================================
# Secrets Management
# ============================================================================

secrets-load:
	@if [ -f config/$(CONTEXT)/load-secrets.sh ]; then \
		echo "🔑 Loading secrets from AWS Secrets Manager..."; \
		. config/$(CONTEXT)/load-secrets.sh; \
	else \
		echo "❌ No secrets loader found at config/$(CONTEXT)/load-secrets.sh"; \
		exit 1; \
	fi

secrets-store:
	@if [ -z "$(SECRET_NAME)" ]; then \
		echo "❌ Error: SECRET_NAME required"; \
		echo "Usage: make secrets-store SECRET_NAME=myproject/config SECRET_FILE=.env"; \
		exit 1; \
	fi
	@if [ ! -f "$(SECRET_FILE)" ]; then \
		echo "❌ Error: SECRET_FILE not found: $(SECRET_FILE)"; \
		exit 1; \
	fi
	@echo "🔐 Storing secrets in AWS Secrets Manager: $(SECRET_NAME)"
	@cat $(SECRET_FILE) | grep -v '^#' | grep -v '^$$' | jq -R -s 'split("\n") | map(select(length > 0) | split("=") | {key: .[0], value: .[1:]|join("=")}) | from_entries' > /tmp/secrets.json
	@aws secretsmanager create-secret \
		--name "$(SECRET_NAME)" \
		--secret-string file:///tmp/secrets.json \
		--profile $(AWS_PROFILE) \
		--region $(AWS_REGION) 2>/dev/null || \
	aws secretsmanager update-secret \
		--secret-id "$(SECRET_NAME)" \
		--secret-string file:///tmp/secrets.json \
		--profile $(AWS_PROFILE) \
		--region $(AWS_REGION)
	@rm /tmp/secrets.json
	@echo "✓ Secrets stored successfully"

# ============================================================================
# Deployment Status & Info
# ============================================================================

infra-status:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Infrastructure Status"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "   Deploy ID: $(DEPLOY_ID)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@if [ -L "$(CURRENT_LINK)" ]; then \
		CURRENT=$$(readlink $(CURRENT_LINK)); \
		echo "Current Release: $$CURRENT"; \
		if [ -f "$(CURRENT_LINK)/manifest.json" ]; then \
			cat $(CURRENT_LINK)/manifest.json | jq .; \
		fi; \
		if [ -f "$(CURRENT_LINK)/outputs.json" ]; then \
			echo ""; \
			echo "Outputs:"; \
			cat $(CURRENT_LINK)/outputs.json | jq .; \
		fi; \
	else \
		echo "No current deployment for $(DEPLOY_ID)"; \
	fi
	@echo ""
	@echo "Recent Releases:"
	@ls -lt $(RELEASES_DIR) 2>/dev/null | head -6 || echo "No releases found"

infra-outputs:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📤 Stack Outputs ($(DEPLOY_ID))"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@if [ -f "$(CURRENT_LINK)/outputs.json" ]; then \
		cat $(CURRENT_LINK)/outputs.json | jq .; \
	else \
		echo "No outputs found. Deploy infrastructure first."; \
	fi

infra-list:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 Available Configurations"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@for ctx_dir in config/*/; do \
		ctx=$$(basename $$ctx_dir); \
		stages=$$(ls $$ctx_dir*.tfvars 2>/dev/null | xargs -n1 basename | sed 's/.tfvars//'); \
		if [ -n "$$stages" ]; then \
			echo "Context: $$ctx"; \
			echo "  Stages: $$stages"; \
			echo ""; \
		fi; \
	done

# ============================================================================
# Help
# ============================================================================

help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "Terraform HCL - Multi-Context/Multi-Stage Infrastructure"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📋 Configuration:"
	@echo "  CONTEXT=[context]             Deployment context (work, personal)"
	@echo "  STAGE=[stage]                 Deployment stage (dev, prod, blue, etc.)"
	@echo "  Default: CONTEXT=work STAGE=dev"
	@echo ""
	@echo "🚀 Deployment:"
	@echo "  make infra-bootstrap          Create state bucket + init Terraform"
	@echo "  make infra-deploy             Plan + apply with release history"
	@echo "  make infra-destroy            Destroy all resources"
	@echo "  make infra-diff               Show pending changes (terraform plan)"
	@echo "  make infra-rollback RELEASE=  Rollback to specific release"
	@echo ""
	@echo "📊 Status & Info:"
	@echo "  make infra-status             Show current deployment status"
	@echo "  make infra-outputs            Show stack outputs"
	@echo "  make infra-list               List available contexts and stages"
	@echo ""
	@echo "🔐 Secrets Management:"
	@echo "  make secrets-load             Load secrets from AWS Secrets Manager"
	@echo "  make secrets-store SECRET_NAME= SECRET_FILE=  Store secrets"
	@echo ""
	@echo "🛠️  Development:"
	@echo "  make init                     Initialize Terraform"
	@echo "  make validate                 Validate configuration"
	@echo "  make plan                     Show execution plan"
	@echo "  make fmt                      Format HCL files"
	@echo "  make lint                     Run tflint"
	@echo ""
	@echo "📖 Examples:"
	@echo "  make infra-deploy CONTEXT=work STAGE=dev"
	@echo "  make infra-deploy CONTEXT=personal STAGE=blue"
	@echo "  make infra-status CONTEXT=work STAGE=prod"
	@echo "  make infra-diff CONTEXT=personal STAGE=alpha"
