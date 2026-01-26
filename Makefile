# Makefile for PySpark ETL Project

.PHONY: help install test run clean lint format docs docker-build docker-run docker-compose-up docker-compose-down docker-logs

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Local Development:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run all tests"
	@echo "  run          - Run the ETL pipeline"
	@echo "  read-output  - Read transformed data"
	@echo "  clean        - Clean up generated files"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  docs         - Generate documentation"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     - Build Docker images"
	@echo "  docker-up        - Start all services (docker-compose up)"
	@echo "  docker-down      - Stop all services (docker-compose down)"
	@echo "  docker-logs      - View logs (docker-compose logs -f)"
	@echo "  docker-ps        - Show running containers"
	@echo "  docker-rebuild   - Rebuild without cache"
	@echo "  docker-clean     - Remove containers and volumes"
	@echo "  docker-backend   - Shell into backend container"
	@echo "  docker-frontend  - Shell into frontend container"

# Installation
install:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/pip install -e .

install-dev:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/pip install -e ".[dev]"

# Testing
test:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/python -m pytest src/tests/ -v --tb=short

test-cov:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/python -m pytest src/tests/ --cov=src --cov-report=html --cov-report=term

# Running
run:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/python -m src.main

read-output:
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	./.venv/bin/python scripts/read_output.py

# Code quality
lint:
	flake8 src/ scripts/
	mypy src/

format:
	black src/ scripts/

# Documentation
docs:
	sphinx-build docs/ docs/_build/html

# Docker Compose Commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

docker-rebuild:
	docker-compose build --no-cache

docker-clean:
	docker-compose down -v --remove-orphans

docker-backend:
	docker-compose exec backend bash

docker-frontend:
	docker-compose exec frontend sh

# Legacy Docker commands
docker-build:
	docker build -t pyspark-etl .

docker-run:
	docker run --rm -v $$(pwd)/data:/app/data -v $$(pwd)/output:/app/output pyspark-etl

# Cleanup
clean:
	rm -rf output/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Development setup
setup-dev: clean
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$$PATH" && \
	pip install -e ".[dev]" && \
	pre-commit install

# CI/CD simulation
ci: lint test

# Production deployment (placeholder)
deploy:
	@echo "Deploying to production..."
	# Add your deployment commands here