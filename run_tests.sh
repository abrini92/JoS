#!/bin/bash
#
# JarvisOS Test Runner
# Runs complete test suite with judge
#

set -e

echo "🧪 JarvisOS Test Suite"
echo "======================"
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo "❌ Virtual environment not found. Run: python -m venv venv"
        exit 1
    fi
fi

# Install test dependencies if needed
echo "📦 Checking test dependencies..."
pip install -q pytest pytest-cov rich 2>/dev/null || true

echo ""
echo "="*60
echo ""

# Run pytest with coverage
echo "🧪 Running Unit Tests..."
echo ""
pytest tests/ -v --cov=jarvisos --cov-report=term-missing --cov-report=html || true

echo ""
echo "="*60
echo ""

# Run the judge
echo "⚖️  Running Test Judge..."
echo ""
python tests/test_judge.py

echo ""
echo "="*60
echo ""

# Summary
echo "✅ Test suite complete!"
echo ""
echo "📊 Reports generated:"
echo "  - test_report.json (Judge report)"
echo "  - htmlcov/index.html (Coverage report)"
echo ""
echo "View coverage: open htmlcov/index.html"
echo ""
