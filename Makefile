.PHONY: install test lint clean

# Install development dependencies
install:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

# Run tests
test:
	@echo "Running tests..."
	pytest tests

# Lint code (optional)
lint:
	@echo "Linting code with flake8..."
	flake8 custom_components tests

# Clean up cache files
clean:
	@echo "Cleaning up cache files..."
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
