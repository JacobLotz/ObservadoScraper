# Makefile for ObservadoScraper

# Python environment
PYTHON=python
CONDA_ENV=observadoscraper
SCRIPT=scripts/migrationtrend.py
MODULE=scripts.migrationtrend
ENV_NAME=envfile
ENV_FILE=environment.yml

# Default task
run:
	@echo "Running script as module..."
	$(PYTHON) -m $(MODULE)

# Set up a new conda environment
setup:
	@echo "Creating Conda environment: $(ENV_NAME)"
	conda env create -f $(ENV_FILE)
	conda activate $(ENV_NAME)

loadenv:
	@echo "Loading Conda environment: $(ENV_NAME)"
	conda activate $(ENV_NAME)

# Clean up __pycache__ files
clean:
	@echo "Cleaning up cache..."
	find . -type d -name '__pycache__' -exec rm -r {} +

# Scrape a migration trend
migtrend:
	python -m scripts.migrationtrend

# Update the ranking
ranking:
	rm -f results.txt results.png
	python -m scripts.updateranking
	pango-view --font=mono -qo results.png results.txt --dpi 150

observations:
	python -m scripts.getobservations

# Testing targets
.PHONY: test test-unit test-integration test-all

# Run unit tests only (fast, no internet required)
test:
	@echo "Running unit tests..."
	conda run -n $(CONDA_ENV) pytest -v

# Alias for test
test-unit: test

# Run integration tests (slow, requires internet, may hit bot detection)
test-integration:
	@echo "Running integration tests..."
	@echo "These tests scrape the real website and may take a while..."
	@echo ""
	@echo "Test 1/4: Normal observation (Gewone Zeehond)..."
	conda run -n $(CONDA_ENV) python tests/verify_mock_382543115.py
	@echo ""
	@echo "Test 2/4: Self-find observation (Vale Gierzwaluw)..."
	conda run -n $(CONDA_ENV) python tests/verify_mock_257848200.py
	@echo ""
	@echo "Test 3/4: Obscured observation (Wolf)..."
	conda run -n $(CONDA_ENV) python tests/verify_mock_obscured.py
	@echo ""
	@echo "Test 4/4: Observations list page..."
	conda run -n $(CONDA_ENV) python tests/verify_mock_list_page.py
	@echo ""
	@echo "All integration tests complete!"

# Run all tests (unit + integration)
test-all: test-unit
	@echo ""
	@echo "Unit tests complete. Starting integration tests..."
	@echo ""
	@$(MAKE) test-integration

# Code style targets
.PHONY: style style-check style-fix lint

# Run all style checks
style-check:
	@echo "Checking code style..."
	@echo ""
	@echo "1. Checking import sorting with isort..."
	conda run -n $(CONDA_ENV) isort --check-only --diff classes/ scripts/ tests/
	@echo ""
	@echo "2. Checking code formatting with black..."
	conda run -n $(CONDA_ENV) black --check classes/ scripts/ tests/
	@echo ""
	@echo "3. Running linter with flake8..."
	conda run -n $(CONDA_ENV) flake8 classes/ scripts/ tests/
	@echo ""
	@echo "All style checks passed!"

# Fix code style automatically
style-fix:
	@echo "Fixing code style..."
	@echo ""
	@echo "1. Sorting imports with isort..."
	conda run -n $(CONDA_ENV) isort classes/ scripts/ tests/
	@echo ""
	@echo "2. Formatting code with black..."
	conda run -n $(CONDA_ENV) black classes/ scripts/ tests/
	@echo ""
	@echo "Code style fixed! Run 'make style-check' to verify."

# Alias for style-fix
style: style-fix

# Run linter only
lint:
	@echo "Running flake8 linter..."
	conda run -n $(CONDA_ENV) flake8 classes/ scripts/ tests/
