.PHONY: install dev build test lint format typecheck clean preview

install:
	npm install

dev:
	npx email dev

build:
	npm run build

test:
	npm test

lint:
	npx eslint src emails --ext .ts,.tsx

format:
	npx prettier --write "src/**/*.{ts,tsx}" "emails/**/*.tsx"

typecheck:
	npx tsc --noEmit

preview:
	npx email dev

check: lint typecheck test

clean:
	rm -rf dist node_modules coverage .react-email
