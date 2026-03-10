.PHONY: install build test lint format typecheck clean synth deploy diff help
.PHONY: infra-bootstrap infra-deploy infra-destroy infra-diff infra-rollback
.PHONY: infra-import infra-import-all infra-import-list infra-status infra-outputs infra-list
.PHONY: secrets-load secrets-store migrate-multi-context

# Configuration
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

# Import tool location
INFRA_IMPORT := python3 ../../shared/tools/infra-import.py

install:
	npm install

build:
	npm run build

test:
	npm test

lint:
	npx eslint lib bin --ext .ts

format:
	npx prettier --write "lib/**/*.ts" "bin/**/*.ts" "test/**/*.ts"

typecheck:
	npx tsc --noEmit

synth:
	npx cdk synth

diff:
	npx cdk diff

deploy:
	npx cdk deploy

check: lint typecheck test

clean:
	rm -rf cdk.out node_modules coverage

# ============================================================================
# Capistrano-style Deployment Management
# ============================================================================

infra-bootstrap:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Bootstrapping CDK"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@mkdir -p $(RELEASE_DIR) $(SHARED_DIR)
	cd infra && CONTEXT=$(CONTEXT) STAGE=$(STAGE) npx cdk bootstrap aws://$(AWS_ACCOUNT_ID)/$(AWS_REGION) 2>&1 | tee ../$(RELEASE_DIR)/bootstrap.log
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
	@if [ -f infra/config/$(CONTEXT)/load-secrets.sh ]; then \
		echo "🔑 Loading secrets from AWS Secrets Manager..."; \
		. infra/config/$(CONTEXT)/load-secrets.sh; \
	fi
	cd infra && CONTEXT=$(CONTEXT) STAGE=$(STAGE) npx cdk deploy --all --require-approval never --outputs-file ../$(RELEASE_DIR)/outputs.json 2>&1 | tee ../$(RELEASE_DIR)/deploy.log
	@ln -sfn releases/$(TIMESTAMP) $(CURRENT_LINK)
	@echo '{"timestamp":"$(TIMESTAMP)","context":"$(CONTEXT)","stage":"$(STAGE)","status":"deployed","git_commit":"$(shell git rev-parse HEAD 2>/dev/null || echo unknown)"}' > $(RELEASE_DIR)/manifest.json
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
		echo "⚠️  Note: This only updates the symlink. You may need to re-deploy."; \
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
	cd infra && CONTEXT=$(CONTEXT) STAGE=$(STAGE) npx cdk destroy --all --force 2>&1 | tee ../$(RELEASE_DIR)/destroy.log
	@echo '{"timestamp":"$(TIMESTAMP)","context":"$(CONTEXT)","stage":"$(STAGE)","status":"destroyed"}' > $(RELEASE_DIR)/manifest.json

infra-diff:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔍 Infrastructure Diff"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd infra && CONTEXT=$(CONTEXT) STAGE=$(STAGE) npx cdk diff

# ============================================================================
# Infrastructure Import (for existing AWS resources)
# ============================================================================

infra-import:
	@if [ -z "$(STACK)" ]; then \
		echo "❌ Error: STACK name required"; \
		echo "Usage: make infra-import STACK=your-stack-name"; \
		exit 1; \
	fi
	@echo "📥 Importing stack: $(STACK)"
	$(INFRA_IMPORT) --stack $(STACK) --profile $(AWS_PROFILE) --region $(AWS_REGION)
	@echo "✓ Import complete. Review infra/config/ and infra/deploys/"

infra-import-all:
	@echo "📥 Importing all stacks..."
	$(INFRA_IMPORT) --all --profile $(AWS_PROFILE) --region $(AWS_REGION)

infra-import-list:
	@echo "📋 Listing CloudFormation stacks..."
	$(INFRA_IMPORT) --list --profile $(AWS_PROFILE) --region $(AWS_REGION)

# ============================================================================
# Secrets Management
# ============================================================================

secrets-load:
	@if [ -f infra/config/load-secrets.sh ]; then \
		echo "🔑 Loading secrets from AWS Secrets Manager..."; \
		. infra/config/load-secrets.sh; \
	else \
		echo "❌ No secrets loader found. Run 'make infra-import' first."; \
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
	@# Convert .env to JSON
	@cat $(SECRET_FILE) | grep -v '^#' | grep -v '^$$' | jq -R -s 'split("\n") | map(select(length > 0) | split("=") | {key: .[0], value: .[1:]|join("=")}) | from_entries' > /tmp/secrets.json
	@# Store in Secrets Manager
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
	@for ctx_dir in infra/config/*/; do \
		ctx=$$(basename $$ctx_dir); \
		stages=$$(ls $$ctx_dir*.yml 2>/dev/null | xargs -n1 basename | sed 's/.yml//'); \
		if [ -n "$$stages" ]; then \
			echo "Context: $$ctx"; \
			echo "  Stages: $$stages"; \
			echo ""; \
		fi; \
	done

# ============================================================================
# Migration
# ============================================================================

migrate-multi-context:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Migrating to Multi-Context Infrastructure"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@if [ -f "../../shared/golden-repos/typescript-cdk/bin/migrate-to-multi-context.py" ]; then \
		python3 ../../shared/golden-repos/typescript-cdk/bin/migrate-to-multi-context.py --context $(CONTEXT); \
	else \
		echo "❌ Migration script not found"; \
		echo "   Please run from a project in the lab monorepo"; \
		exit 1; \
	fi

# ============================================================================
# Help
# ============================================================================

help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "Infrastructure Management - Multi-Context/Multi-Stage"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📋 Configuration:"
	@echo "  CONTEXT=[context]             Deployment context (work, personal)"
	@echo "  STAGE=[stage]                 Deployment stage (dev, prod, blue, etc.)"
	@echo "  Default: CONTEXT=work STAGE=dev"
	@echo ""
	@echo "🚀 Deployment:"
	@echo "  make infra-bootstrap          Bootstrap CDK (one-time per account)"
	@echo "  make infra-deploy             Deploy infrastructure"
	@echo "  make infra-destroy            Destroy all resources"
	@echo "  make infra-diff               Show pending changes"
	@echo "  make infra-rollback RELEASE=  Rollback to specific release"
	@echo ""
	@echo "📊 Status & Info:"
	@echo "  make infra-status             Show current deployment status"
	@echo "  make infra-outputs            Show stack outputs (ARNs, URLs)"
	@echo "  make infra-list               List available contexts and stages"
	@echo ""
	@echo "📥 Import Existing Infrastructure:"
	@echo "  make infra-import STACK=name  Import existing CloudFormation stack"
	@echo "  make infra-import-all         Import all stacks in account"
	@echo "  make infra-import-list        List all CloudFormation stacks"
	@echo ""
	@echo "🔐 Secrets Management:"
	@echo "  make secrets-load             Load secrets from AWS Secrets Manager"
	@echo "  make secrets-store SECRET_NAME= SECRET_FILE=  Store secrets"
	@echo ""
	@echo "🛠️  Development:"
	@echo "  make install                  Install dependencies"
	@echo "  make build                    Build project"
	@echo "  make test                     Run tests"
	@echo "  make synth                    Synthesize CloudFormation"
	@echo ""
	@echo "🔄 Migration:"
	@echo "  make migrate-multi-context    Migrate existing project to multi-context"
	@echo ""
	@echo "📖 Examples:"
	@echo "  make infra-deploy CONTEXT=work STAGE=dev"
	@echo "  make infra-deploy CONTEXT=personal STAGE=blue"
	@echo "  make infra-status CONTEXT=work STAGE=prod"
	@echo "  make infra-diff CONTEXT=personal STAGE=alpha"
	@echo "  make migrate-multi-context CONTEXT=work"
