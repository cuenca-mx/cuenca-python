# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```
# Create a virtual environment
python3.13 -m venv --prompt cuenca venv

# Activate the virtual environment (bash/zsh)
source venv/bin/activate

# Install dependencies
pip install -qU -r requirements.txt
pip install -qU -r requirements-test.txt
```

### Testing
```
# Run all tests
pytest

# Run a single test
pytest tests/resources/test_transfers.py::test_transfers_create

# Run tests with VCR recording
pytest --vcr-record=all tests/resources/test_transfers.py

# Run tests with coverage
pytest --cov=cuenca
```

### Linting and Formatting
```
# Format code
make format

# Run linters (flake8, isort, black, mypy)
make lint

# Clean project
make clean
```

### Building and Publishing
```
# Build package
python setup.py sdist bdist_wheel

# Release to PyPI (after running tests)
make release
```

## Code Architecture

### Overview
Cuenca Python is a client library for interacting with the Cuenca API. The library is built around a resource-based architecture using Pydantic models for data validation and type safety.

### Key Components

1. **HTTP Client (`cuenca/http/`)**: 
   - Handles API requests, authentication, and response processing
   - Supports both basic auth and JWT authentication
   - Configurable for sandbox or production environments

2. **Resources (`cuenca/resources/`)**: 
   - Resource classes represent API entities like Transfers, Users, Cards, etc.
   - Base classes provide common functionality (Retrievable, Creatable, Queryable, etc.)
   - All resources are exposed through the root package imports

3. **Authentication**:
   - Configuration via environment variables (CUENCA_API_KEY, CUENCA_API_SECRET)
   - Manual configuration via `cuenca.configure()`
   - JWT token support with automatic renewal

4. **Query System**:
   - Fluent interface for querying resources
   - Methods: `one()`, `first()`, `all()`, `count()`
   - Automatic pagination handling

### Testing Architecture

1. **VCR Testing**: 
   - Uses pytest-vcr to record and replay HTTP interactions
   - Cassettes stored in tests/resources/cassettes/
   - Filters sensitive authentication headers

2. **Fixtures**:
   - Common test data and setup in tests/conftest.py
   - Resource-specific fixtures in test files

### Error Handling

- Custom exceptions for API errors
- Validation errors from Pydantic
- Query errors (NoResultFound, MultipleResultsFound)