.PHONY: install dev build start test lint format typecheck clean buildinfo

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
# For Next.js, output to public/ so it's served statically
buildinfo:
	@if [ -f "$(CDK_OUTPUTS)" ]; then \
		python3 $(SHARED_TOOLS)/generate-buildinfo.py \
			--output public/buildinfo.json \
			--cdk-outputs $(CDK_OUTPUTS) \
			--project-id $(PROJECT_ID) \
			--environment $(ENVIRONMENT); \
	else \
		python3 $(SHARED_TOOLS)/generate-buildinfo.py \
			--output public/buildinfo.json \
			--project-id $(PROJECT_ID) \
			--environment $(ENVIRONMENT); \
	fi

# Build with buildinfo (generate before build so it's included)
build-with-info: buildinfo build

start:
	npm start

test:
	npm test

lint:
	npm run lint

format:
	npx prettier --write "src/**/*.{ts,tsx}"

typecheck:
	npx tsc --noEmit

check: lint typecheck test

clean:
	rm -rf .next node_modules coverage out
