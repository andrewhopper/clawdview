.PHONY: install install-all build build-backend build-frontend dev test lint clean \
        infra-bootstrap infra-deploy infra-destroy infra-diff infra-synth infra-rollback \
        setup-auth-params verify-auth-params

# Configuration
TIMESTAMP := $(shell date +%Y%m%d-%H%M)
RELEASES_DIR := infra/deploys/releases
RELEASE_DIR := $(RELEASES_DIR)/$(TIMESTAMP)
CURRENT_LINK := infra/deploys/current
KEEP_RELEASES := 5

# Default target
.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# Installation
# ============================================

install: ## Install all dependencies
	npm install
	cd infra && npm install
	cd backend && npm install
	cd frontend && npm install
	cd backend-python && pip install -r requirements.txt

install-all: install ## Alias for install

# ============================================
# Development
# ============================================

dev: ## Start frontend development server
	cd frontend && npm run dev

dev-backend: ## Build and watch backend
	cd backend && npm run watch

# ============================================
# Build
# ============================================

build: build-backend build-frontend ## Build all

build-backend: ## Build TypeScript backend
	cd backend && npm run build

build-frontend: ## Build frontend for production
	cd frontend && npm run build

# ============================================
# Testing & Linting
# ============================================

test: ## Run all tests
	cd backend && npm test
	cd backend-python && pytest

lint: ## Run linters
	cd backend && npm run lint
	cd frontend && npm run lint
	cd backend-python && ruff check src

typecheck: ## Run type checking
	cd backend && npm run typecheck
	cd frontend && npm run typecheck
	cd backend-python && mypy src

# ============================================
# Infrastructure
# ============================================

infra-bootstrap: ## Bootstrap CDK for AWS account/region
	@echo "Bootstrapping CDK..."
	@mkdir -p $(RELEASE_DIR) infra/deploys/shared
	cd infra && npm run bootstrap 2>&1 | tee ../$(RELEASE_DIR)/bootstrap.log
	@echo "CDK bootstrap complete"

infra-synth: ## Synthesize CDK stack
	cd infra && npm run synth

infra-diff: ## Show infrastructure changes
	cd infra && npm run cdk diff

infra-deploy: build-backend ## Deploy infrastructure
	@echo "Deploying infrastructure to $(RELEASE_DIR)..."
	@mkdir -p $(RELEASE_DIR) infra/deploys/shared
	cd infra && npm run deploy -- --outputs-file ../$(RELEASE_DIR)/outputs.json 2>&1 | tee ../$(RELEASE_DIR)/deploy.log
	@ln -sfn releases/$(TIMESTAMP) $(CURRENT_LINK)
	@echo '{"timestamp":"$(TIMESTAMP)","status":"deployed"}' > $(RELEASE_DIR)/manifest.json
	@echo ""
	@echo "Deployed successfully!"
	@echo "Release: $(RELEASE_DIR)"
	@echo ""
	@echo "Stack outputs:"
	@cat $(RELEASE_DIR)/outputs.json 2>/dev/null || echo "No outputs file found"
	@# Cleanup old releases (keep last N)
	@cd $(RELEASES_DIR) 2>/dev/null && ls -t | tail -n +$$(($(KEEP_RELEASES)+1)) | xargs -r rm -rf || true

infra-rollback: ## Rollback to previous release
	@echo "Available releases:"
	@ls -t $(RELEASES_DIR) 2>/dev/null | head -$(KEEP_RELEASES) || echo "No releases found"
	@echo ""
	@echo "Usage: make infra-rollback RELEASE=YYYYMMDD-HHMM"
ifdef RELEASE
	@if [ -d "$(RELEASES_DIR)/$(RELEASE)" ]; then \
		ln -sfn releases/$(RELEASE) $(CURRENT_LINK); \
		echo "Rolled back to $(RELEASE)"; \
	else \
		echo "Release $(RELEASE) not found"; \
		exit 1; \
	fi
endif

infra-destroy: ## Destroy infrastructure
	@echo "WARNING: This will destroy all infrastructure!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	@mkdir -p $(RELEASE_DIR)
	cd infra && npm run destroy 2>&1 | tee ../$(RELEASE_DIR)/destroy.log

# ============================================
# Utilities
# ============================================

clean: ## Clean build artifacts
	rm -rf backend/dist
	rm -rf frontend/dist
	rm -rf infra/cdk.out
	rm -rf node_modules
	rm -rf backend/node_modules
	rm -rf frontend/node_modules
	rm -rf infra/node_modules
	rm -rf backend-python/__pycache__
	rm -rf backend-python/.pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

outputs: ## Show current deployment outputs
	@cat $(CURRENT_LINK)/outputs.json 2>/dev/null || echo "No current deployment found"

logs: ## Show recent deployment logs
	@tail -50 $(CURRENT_LINK)/deploy.log 2>/dev/null || echo "No deployment logs found"

update-frontend-env: ## Update frontend .env from CDK outputs
	@if [ -f "$(CURRENT_LINK)/outputs.json" ]; then \
		echo "Updating frontend/.env.local from CDK outputs..."; \
		node -e " \
			const outputs = require('./$(CURRENT_LINK)/outputs.json'); \
			const stack = Object.keys(outputs)[0]; \
			const vals = outputs[stack]; \
			console.log('VITE_API_URL=' + vals.ApiUrl); \
			console.log('VITE_USER_POOL_ID=' + vals.UserPoolId); \
			console.log('VITE_USER_POOL_CLIENT_ID=' + vals.UserPoolClientId); \
		" > frontend/.env.local; \
		echo "Updated frontend/.env.local"; \
	else \
		echo "No CDK outputs found. Run 'make infra-deploy' first."; \
	fi

# ============================================
# Auth Configuration (SSM Parameter Store)
# ============================================

setup-auth-params: ## Setup SSM parameters for shared auth (auth.b.lfg.new)
	@echo "Setting up SSM parameters for shared auth configuration..."
	python3 scripts/setup-auth-params.py $(if $(AWS_PROFILE),--profile $(AWS_PROFILE)) $(if $(AWS_REGION),--region $(AWS_REGION))

verify-auth-params: ## Verify SSM auth parameters exist
	@echo "Verifying SSM auth parameters..."
	python3 scripts/setup-auth-params.py --verify-only $(if $(AWS_PROFILE),--profile $(AWS_PROFILE)) $(if $(AWS_REGION),--region $(AWS_REGION))
