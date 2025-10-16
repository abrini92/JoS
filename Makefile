# JarvisOS Makefile
# Quick commands for common tasks

.PHONY: help install test clean run status

help:
	@echo "JarvisOS - Available Commands"
	@echo "=============================="
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run installation tests"
	@echo "  make status     - Show system status"
	@echo "  make observe    - Quick observation (30s)"
	@echo "  make analyze    - Analyze observations"
	@echo "  make generate   - Generate automation"
	@echo "  make clean      - Clean generated files"
	@echo "  make demo       - Run full demo workflow"
	@echo ""

install:
	@echo "Installing JarvisOS..."
	./setup.sh

test:
	@echo "Testing installation..."
	python3 test_installation.py

status:
	@echo "Checking JarvisOS status..."
	python jarvis.py status

observe:
	@echo "Starting observation (30s)..."
	python jarvis.py observe --duration 30 --interval 5

analyze:
	@echo "Analyzing observations..."
	python jarvis.py analyze

generate:
	@echo "Generating automation..."
	python jarvis.py generate

list:
	@echo "Listing scripts..."
	python jarvis.py list

clean:
	@echo "Cleaning generated files..."
	rm -rf data/ generated_scripts/ logs/
	rm -rf __pycache__ jarvisos/__pycache__ jarvisos/core/__pycache__
	find . -name "*.pyc" -delete
	@echo "Clean complete!"

demo:
	@echo "Running full demo workflow..."
	@echo ""
	@echo "Step 1: Observe (30s)..."
	python jarvis.py observe --duration 30 --interval 5
	@echo ""
	@echo "Step 2: Analyze..."
	python jarvis.py analyze
	@echo ""
	@echo "Step 3: Generate..."
	python jarvis.py generate
	@echo ""
	@echo "Step 4: List scripts..."
	python jarvis.py list
	@echo ""
	@echo "Demo complete! Run 'python jarvis.py run 1 --dry-run' to preview"

lint:
	@echo "Linting code..."
	python -m py_compile jarvis.py
	python -m py_compile jarvisos/core/*.py
	@echo "Syntax check passed!"

check: test lint
	@echo "All checks passed!"

test-verbose:
	@echo "Running tests with verbose output..."
	python -m pytest tests/ -v

test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tests/ --cov=jarvisos --cov-report=html --cov-report=term

test-watch:
	@echo "Running tests in watch mode..."
	python -m pytest tests/ -f
