.PHONY: install dev build preview test lint format typecheck clean buildinfo

# Path to shared tools (adjust if needed)
SHARED_TOOLS ?= ../../shared/tools
PROJECT_ID ?= $(shell basename $(CURDIR))
ENVIRONMENT ?= dev
CDK_OUTPUTS ?= infra/deploys/current/outputs.json

install:
	npm install

dev:
	npm run dev

build:
	npm run build

# Generate buildinfo.json with deployment metadata
buildinfo:
	@if [ -f "$(CDK_OUTPUTS)" ]; then \
		python3 $(SHARED_TOOLS)/generate-buildinfo.py \
			--output dist/buildinfo.json \
			--cdk-outputs $(CDK_OUTPUTS) \
			--project-id $(PROJECT_ID) \
			--environment $(ENVIRONMENT); \
	else \
		python3 $(SHARED_TOOLS)/generate-buildinfo.py \
			--output dist/buildinfo.json \
			--project-id $(PROJECT_ID) \
			--environment $(ENVIRONMENT); \
	fi

# Build with buildinfo
build-with-info: build buildinfo

preview:
	npm run preview

test:
	npm test

test-watch:
	npm run test:watch

lint:
	npx eslint src --ext .ts,.tsx

format:
	npx prettier --write "src/**/*.{ts,tsx}"

typecheck:
	npx tsc --noEmit

check: lint typecheck test

clean:
	rm -rf dist node_modules coverage
