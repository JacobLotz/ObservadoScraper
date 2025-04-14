# Makefile for ObservadoScraper

# Python environment
PYTHON=python
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

test:
	pytest
