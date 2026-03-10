.PHONY: install test lint format typecheck clean run

install:
	uv sync

run:
	uv run python -m src.main

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

typecheck:
	uv run mypy src

check: lint typecheck test

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache __pycache__ .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
