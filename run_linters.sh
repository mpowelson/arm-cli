#!/bin/bash

# ARM CLI Linting Script
# This script runs all configured linters for the arm-cli project using Poetry

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the arm-cli root directory."
    exit 1
fi

print_status "Starting linting checks for arm-cli..."

# Check if Poetry is installed
if ! command -v poetry > /dev/null 2>&1; then
    print_error "Poetry is not installed. Please install Poetry first:"
    echo "  curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if Poetry environment is set up
if [ ! -f "poetry.lock" ]; then
    print_status "Poetry lock file not found. Installing dependencies..."
    poetry install --with dev
else
    print_status "Installing/updating dependencies..."
    poetry install --with dev
fi

# Run Black (code formatter)
print_status "Running Black (code formatter)..."
if poetry run black --check .; then
    print_success "Black check passed - code is properly formatted"
else
    print_error "Black check failed - code needs formatting"
    print_status "Run 'poetry run black .' to automatically format the code"
    BLACK_FAILED=true
fi

# Run isort (import sorter)
print_status "Running isort (import sorter)..."
if poetry run isort --check-only .; then
    print_success "isort check passed - imports are properly sorted"
else
    print_error "isort check failed - imports need sorting"
    print_status "Run 'poetry run isort .' to automatically sort imports"
    ISORT_FAILED=true
fi

# Run Flake8 (style checker)
print_status "Running Flake8 (style checker)..."
if poetry run flake8 .; then
    print_success "Flake8 check passed - no style issues found"
else
    print_error "Flake8 check failed - style issues found"
    FLAKE8_FAILED=true
fi

# Run MyPy (type checker)
print_status "Running MyPy (type checker)..."
if poetry run mypy .; then
    print_success "MyPy check passed - no type issues found"
else
    print_error "MyPy check failed - type issues found"
    MYPY_FAILED=true
fi

# Summary
echo
print_status "Linting Summary:"
if [ "$BLACK_FAILED" = true ] || [ "$ISORT_FAILED" = true ] || [ "$FLAKE8_FAILED" = true ] || [ "$MYPY_FAILED" = true ]; then
    print_error "Some linting checks failed!"
    echo
    print_status "To fix formatting issues:"
    echo "  poetry run black ."
    echo "  poetry run isort ."
    echo
    print_status "To run individual linters:"
    echo "  poetry run flake8 ."
    echo "  poetry run mypy ."
    exit 1
else
    print_success "All linting checks passed! 🎉"
fi 