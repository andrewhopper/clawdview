# Port Management - Auto-allocation and Configuration Sync
# File UUID: b8c9d0e1-f2a3-4b5c-6d7e-8f9a0b1c2d3e
#
# Include this in project Makefiles to enable auto-port allocation
#
# Usage:
#   include $(MONOREPO_ROOT)/shared/standards/ports.mk
#
# Features:
#   - Auto-allocates unique ports on first `make dev`
#   - Persists to repo-wide port_alloc.yml
#   - Auto-generates .env files for all environments
#   - Auto-updates backend CORS configuration

# Get monorepo root
MONOREPO_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null || echo ".")
PORT_MANAGER := $(MONOREPO_ROOT)/bin/port-manager.py

# Auto-detect project ID from directory name (format: name-pXXXX)
PROJECT_ID := $(shell basename $(CURDIR) | grep -oE '[a-z0-9-]+-p[a-z0-9]+$$' || echo "")

# Validate project ID
ifeq ($(PROJECT_ID),)
  $(warning ⚠️  Cannot detect project ID from directory name: $(CURDIR))
  $(warning Expected format: name-pXXXX (e.g., ppm-p1m2n))
  $(warning Port allocation will be skipped.)
endif

# Get or allocate ports (lazy evaluation)
ifneq ($(PROJECT_ID),)
  FRONTEND_PORT = $(shell $(PORT_MANAGER) allocate $(PROJECT_ID) frontend 2>/dev/null || echo "3000")
  BACKEND_PORT = $(shell $(PORT_MANAGER) allocate $(PROJECT_ID) backend 2>/dev/null || echo "4000")
endif

# Export for sub-makes and shell scripts
export FRONTEND_PORT
export BACKEND_PORT
export PROJECT_ID

# ========================================
# Port Management Targets
# ========================================

.PHONY: show-ports
show-ports:
	@$(PORT_MANAGER) show $(PROJECT_ID)

.PHONY: sync-config
sync-config:
	@echo "🔄 Syncing configuration for $(PROJECT_ID)..."
	@$(PORT_MANAGER) sync-env $(PROJECT_ID)
	@$(PORT_MANAGER) sync-backend $(PROJECT_ID)
	@echo "✅ Configuration synced"

.PHONY: check-port-conflicts
check-port-conflicts:
	@echo "🔍 Checking for port conflicts..."
	@for port in $(FRONTEND_PORT) $(BACKEND_PORT); do \
		if lsof -i :$$port > /dev/null 2>&1; then \
			echo "⚠️  Port $$port is in use:"; \
			lsof -i :$$port; \
		fi \
	done
	@echo "✅ Check complete"

.PHONY: show-all-ports
show-all-ports:
	@$(PORT_MANAGER) list
