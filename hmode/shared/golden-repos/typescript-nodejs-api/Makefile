.PHONY: install dev build test lint format typecheck clean

install:
	npm install

dev:
	npm run dev

build:
	npm run build

start:
	npm start

test:
	npm test

test-watch:
	npm run test:watch

test-cov:
	npm run test:coverage

lint:
	npm run lint

format:
	npx prettier --write "src/**/*.ts" "tests/**/*.ts"

typecheck:
	npm run typecheck

check: lint typecheck test

clean:
	rm -rf dist node_modules coverage .turbo
