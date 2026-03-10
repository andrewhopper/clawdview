# Makefile.testing.mk - Standard Testing Targets
# File UUID: 2a4b6c8d-1e3f-5a7b-9c0d-2e4f6a8b0c1d
#
# Include this in your project Makefile:
#   include $(SHARED_DIR)/standards/testing/templates/Makefile.testing.mk
#
# Or copy the relevant sections into your project Makefile.

# ============================================================================
# CONFIGURATION (All Parameterized - Override via environment or make args)
# ============================================================================

# Test URLs and endpoints
TEST_BASE_URL ?= http://localhost:3000
TEST_API_URL ?= $(TEST_BASE_URL)/api

# Coverage and quality thresholds
TEST_COVERAGE_THRESHOLD ?= 70

# Timing configuration
TEST_TIMEOUT ?= 30000
TEST_RETRIES ?= 2

# Execution behavior
TEST_FAIL_FAST ?= true
TEST_PARALLEL ?= true

# Output directories
TEST_REPORT_DIR ?= ./test-reports
TEST_COVERAGE_DIR ?= $(TEST_REPORT_DIR)/coverage

# Git verification (for smoke tests)
EXPECTED_GIT_HASH ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Detect project type (override if needed)
PROJECT_TYPE ?= $(if $(wildcard package.json),node,$(if $(wildcard pyproject.toml),python,$(if $(wildcard requirements.txt),python,unknown)))

# ============================================================================
# INTERNAL FLAGS (derived from configuration)
# ============================================================================

# Vitest flags
VITEST_FLAGS := --reporter=verbose
ifeq ($(TEST_FAIL_FAST),true)
  VITEST_FLAGS += --bail=1
endif
ifdef CI
  VITEST_FLAGS += --coverage --coverage.reporter=json --coverage.reporter=html
endif

# Playwright flags
PLAYWRIGHT_FLAGS := --reporter=junit,html
ifdef CI
  PLAYWRIGHT_FLAGS += --retries=$(TEST_RETRIES)
endif
ifeq ($(TEST_PARALLEL),false)
  PLAYWRIGHT_FLAGS += --workers=1
endif

# Pytest flags
PYTEST_FLAGS := -v
ifeq ($(TEST_FAIL_FAST),true)
  PYTEST_FLAGS += -x
endif
ifdef CI
  PYTEST_FLAGS += --cov --cov-report=xml --cov-report=html
  PYTEST_FLAGS += --cov-fail-under=$(TEST_COVERAGE_THRESHOLD)
  PYTEST_FLAGS += --junitxml=$(TEST_REPORT_DIR)/junit.xml
endif

# ============================================================================
# TESTING TARGETS (Required for all projects)
# ============================================================================

.PHONY: test test-unit test-e2e test-smoke test-coverage test-ci lint test-watch test-debug

## Run ALL tests (unit + e2e)
test: test-unit test-e2e
	@echo "All tests passed"

## Run unit tests only
test-unit: _ensure-report-dir
ifeq ($(PROJECT_TYPE),node)
	@echo "Running unit tests (Node.js)..."
	npx vitest run $(VITEST_FLAGS) --outputFile=$(TEST_REPORT_DIR)/junit.xml
else ifeq ($(PROJECT_TYPE),python)
	@echo "Running unit tests (Python)..."
	pytest tests/unit $(PYTEST_FLAGS)
else
	@echo "ERROR: Unknown project type. Set PROJECT_TYPE=node or PROJECT_TYPE=python"
	@exit 1
endif

## Run end-to-end/integration tests
test-e2e: _ensure-report-dir
	@echo "Running E2E tests..."
ifeq ($(PROJECT_TYPE),node)
	BASE_URL=$(TEST_BASE_URL) \
	npx playwright test $(PLAYWRIGHT_FLAGS) --output=$(TEST_REPORT_DIR)/playwright
else ifeq ($(PROJECT_TYPE),python)
	TEST_BASE_URL=$(TEST_BASE_URL) \
	pytest tests/e2e $(PYTEST_FLAGS)
endif

## Run post-deploy smoke tests (requires TEST_BASE_URL to be set to deployed app)
test-smoke: _ensure-report-dir
	@echo "Running smoke tests against $(TEST_BASE_URL)..."
	@echo "Expected git hash: $(EXPECTED_GIT_HASH)"
ifeq ($(PROJECT_TYPE),node)
	EXPECTED_GIT_HASH=$(EXPECTED_GIT_HASH) \
	BASE_URL=$(TEST_BASE_URL) \
	npx playwright test tests/smoke.spec.ts $(PLAYWRIGHT_FLAGS) --output=$(TEST_REPORT_DIR)/smoke
else ifeq ($(PROJECT_TYPE),python)
	TEST_BASE_URL=$(TEST_BASE_URL) \
	EXPECTED_GIT_HASH=$(EXPECTED_GIT_HASH) \
	pytest tests/smoke $(PYTEST_FLAGS)
endif
	@echo "Smoke tests passed"

## Run tests with coverage report (enforces threshold)
test-coverage: _ensure-report-dir
	@echo "Running tests with coverage (threshold: $(TEST_COVERAGE_THRESHOLD)%)..."
ifeq ($(PROJECT_TYPE),node)
	npx vitest run --coverage \
		--coverage.thresholds.lines=$(TEST_COVERAGE_THRESHOLD) \
		--coverage.thresholds.branches=$(TEST_COVERAGE_THRESHOLD) \
		--coverage.thresholds.functions=$(TEST_COVERAGE_THRESHOLD) \
		--coverage.reportsDirectory=$(TEST_COVERAGE_DIR)
else ifeq ($(PROJECT_TYPE),python)
	pytest --cov \
		--cov-fail-under=$(TEST_COVERAGE_THRESHOLD) \
		--cov-report=html:$(TEST_COVERAGE_DIR) \
		--cov-report=xml:$(TEST_COVERAGE_DIR)/coverage.xml
endif
	@echo "Coverage report: $(TEST_COVERAGE_DIR)/index.html"

## Run tests in CI mode (lint + coverage + e2e, stricter settings)
test-ci: lint test-coverage test-e2e
	@echo "CI tests complete"

## Run linter (language-specific)
lint:
	@echo "Running linter..."
ifeq ($(PROJECT_TYPE),node)
	npx eslint . --max-warnings=0
	npx tsc --noEmit
else ifeq ($(PROJECT_TYPE),python)
	ruff check .
	mypy . || true
endif

## Watch mode for development (auto-runs on file changes)
test-watch:
	@echo "Starting test watch mode..."
ifeq ($(PROJECT_TYPE),node)
	npx vitest
else ifeq ($(PROJECT_TYPE),python)
	pip install pytest-watch 2>/dev/null || true
	ptw
endif

## Debug mode (headed browser, step through)
test-debug:
	@echo "Starting debug mode..."
	npx playwright test --debug

# ============================================================================
# HELPER TARGETS
# ============================================================================

_ensure-report-dir:
	@mkdir -p $(TEST_REPORT_DIR)
	@mkdir -p $(TEST_COVERAGE_DIR)

## Show current test configuration
test-config:
	@echo "=== Test Configuration ==="
	@echo "PROJECT_TYPE:            $(PROJECT_TYPE)"
	@echo "TEST_BASE_URL:           $(TEST_BASE_URL)"
	@echo "TEST_COVERAGE_THRESHOLD: $(TEST_COVERAGE_THRESHOLD)%"
	@echo "TEST_TIMEOUT:            $(TEST_TIMEOUT)ms"
	@echo "TEST_RETRIES:            $(TEST_RETRIES)"
	@echo "TEST_FAIL_FAST:          $(TEST_FAIL_FAST)"
	@echo "TEST_PARALLEL:           $(TEST_PARALLEL)"
	@echo "TEST_REPORT_DIR:         $(TEST_REPORT_DIR)"
	@echo "EXPECTED_GIT_HASH:       $(EXPECTED_GIT_HASH)"
	@echo "CI:                      $(CI)"

## Clean test artifacts
test-clean:
	@echo "Cleaning test artifacts..."
	rm -rf $(TEST_REPORT_DIR)
	rm -rf coverage
	rm -rf .nyc_output
	rm -rf playwright-report
	rm -rf test-results

## Open coverage report in browser
test-report:
	@echo "Opening coverage report..."
ifeq ($(shell uname),Darwin)
	open $(TEST_COVERAGE_DIR)/index.html
else
	xdg-open $(TEST_COVERAGE_DIR)/index.html 2>/dev/null || echo "Open $(TEST_COVERAGE_DIR)/index.html"
endif

## Show test help
test-help:
	@echo "=== Testing Targets ==="
	@echo "  make test          - Run all tests (unit + e2e)"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-e2e      - Run E2E tests"
	@echo "  make test-smoke    - Run post-deploy smoke tests"
	@echo "  make test-coverage - Run tests with coverage"
	@echo "  make test-ci       - Run CI tests (lint + coverage + e2e)"
	@echo "  make lint          - Run linter"
	@echo "  make test-watch    - Watch mode for development"
	@echo "  make test-debug    - Debug mode with headed browser"
	@echo "  make test-config   - Show current configuration"
	@echo "  make test-clean    - Clean test artifacts"
	@echo "  make test-report   - Open coverage report"
	@echo ""
	@echo "=== Configuration (via env vars) ==="
	@echo "  TEST_BASE_URL           - App URL (default: http://localhost:3000)"
	@echo "  TEST_COVERAGE_THRESHOLD - Min coverage % (default: 70)"
	@echo "  TEST_TIMEOUT            - Timeout in ms (default: 30000)"
	@echo "  TEST_FAIL_FAST          - Stop on first failure (default: true)"
	@echo "  CI                      - Set to enable CI mode"
