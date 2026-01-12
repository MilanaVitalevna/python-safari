.PHONY: help install install-no-dev lint lint-fix format-check format check fix type-check security

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install all dependencies (with dev)
	uv sync

install-no-dev:  ## Install only production dependencies (no dev)
	uv sync --no-dev

run:  ## Run app
	uv run -m src.safari.main

lint:  ## Check code for errors and style issues
	uv run ruff check .

lint-fix:  ## Fix automatically fixable linting issues
	uv run ruff check --fix .

format-check:  ## Check if code is properly formatted
	uv run ruff format --check .

format:  ## Auto-format code
	uv run ruff format .

check: lint format-check  ## Run all checks (lint + format)

fix: lint-fix format  ## Fix all issues (lint + format)

type-check:  ## Run Ty for faster type checking
	uv run ty check src/

security:  ## Security check
	uv run bandit -c pyproject.toml -r src/

test:  ## Run tests
	uv run pytest tests/
