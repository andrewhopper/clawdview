.PHONY: install start ios android web test lint format typecheck clean

install:
	npm install

start:
	npx expo start

ios:
	npx expo start --ios

android:
	npx expo start --android

web:
	npx expo start --web

test:
	npm test

lint:
	npx eslint src app --ext .ts,.tsx

format:
	npx prettier --write "src/**/*.{ts,tsx}" "app/**/*.{ts,tsx}"

typecheck:
	npx tsc --noEmit

check: lint typecheck test

clean:
	rm -rf node_modules .expo dist
