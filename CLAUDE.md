# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ObservadoScraper is a Python-based web scraper for waarneming.nl (Dutch nature observation platform). It scrapes species observations, migration trends, and competition rankings, outputting data to KML files and text reports.

**Architecture**: Modular design separating data gathering (scrapers) from data processing (processors), with pandas DataFrames as the intermediate format.

## Environment Setup

Uses Conda for environment management:
```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate observadoscraper

# Set PYTHONPATH for module imports
export PYTHONPATH=$(pwd)
```

Key dependencies: selenium, BeautifulSoup4, simplekml, webdriver_manager, matplotlib, pandas

## Running Scripts

**Important**: Always run scripts as modules to ensure proper imports:

```bash
# Run as modules (recommended)
python -m scripts.migrationtrend
python -m scripts.updateranking
python -m scripts.getobservations

# Or use Makefile
make test
make migtrend
make ranking
make observations
make clean
```

**Output Location**: All output files (CSV, KML, TXT, PNG) are saved to the `results/` directory, which is created automatically and git-ignored.

## Testing

```bash
# Run all tests (36 tests, fast with mocks)
pytest

# Run specific test categories
pytest tests/test_observation_processor.py  # Processor tests with CSV mocks
pytest tests/test_observation_scraper.py    # Scraper tests with HTML mocks

# Run legacy integration tests (slow, requires live scraping)
pytest -m integration
```

**Test Coverage**: 36 passing tests using HTML and CSV mocks. No live scraping needed for unit tests.

**CI Setup**: GitHub Actions workflow (`.github/workflows/python-tests.yml`) mocks passwords using `tests/mocks/passwords.py`. For local testing, create `passwords/passwords.py` based on `passwords/passwords-example.py`.

## Architecture

### Modular Design (New - Use This)

**Workflow**: Scrape → Save CSV → Load CSV → Process → Export

#### Scrapers (Data Gathering)

1. **`ObservationScraper`** (`classes/observation_scraper.py`)
   - Scrapes single observation page
   - Returns dict with observation data
   - Used internally by ObservationCollectionScraper

2. **`ObservationCollectionScraper`** (`classes/observation_collection_scraper.py`)
   - Scrapes multiple observations from paginated pages
   - Returns pandas DataFrame
   - Methods: `scrape()`, `save()`, `load()`
   - Supports species filtering during scraping

3. **`MigrationScraper`** (`classes/migration_scraper.py`)
   - Scrapes migration trend data from grid maps
   - Returns pandas DataFrame with grid square counts
   - Methods: `scrape_date_ranges()`, `save()`, `load()`

#### Processors (Data Processing)

1. **`ObservationProcessor`** (`classes/observation_processor.py`)
   - Processes observation DataFrames
   - Key methods:
     - `filter_selffinds()` - Filter by self-find markers
     - `assign_points(points_file)` - Assign point values from JSON
     - `filter_by_species(species_list)` - Filter by species
     - `sort_by_date(ascending)` - Sort chronologically
     - `to_kml(filename)` - Export to KML (saves to results/)
     - `to_text_report(filename)` - Export to text report (saves to results/)
     - `get_summary()` - Get statistics
   - Supports method chaining

2. **`MigrationProcessor`** (`classes/migration_processor.py`)
   - Processes migration trend DataFrames
   - Key methods:
     - `plot_species_trend(species_name, month_start, month_end)` - Generate plots (saves to results/)
     - `get_summary()` - Get statistics

#### Utility Functions

- **`get_results_path(filename)`** - Returns full path to file in `results/` directory
- **`ensure_results_dir()`** - Creates `results/` directory if needed

#### Usage Example

```python
from classes import ObservationCollectionScraper, ObservationProcessor

# 1. Scrape data
scraper = ObservationCollectionScraper(link)
df = scraper.scrape()

# 2. Save to results/
scraper.save(df, "observations.csv")

# 3. Process (can be done later, separately)
processor = ObservationProcessor(df)
processor.filter_selffinds().assign_points().to_kml("selffinds.kml")
```

### Legacy Classes (Still Available)

- **`classes/obs.py:Observation`** - Individual observation (legacy)
- **`classes/obscol.py:ObsCollection`** - Collection of observations (legacy)
- **`classes/mig.py:MigClass`** - Migration trend data (legacy)

**Note**: New code should use the modular scrapers/processors. Legacy classes maintained for backward compatibility.

### Base Class

**`classes/base.py:ScrapeBase`**
- Manages Selenium WebDriver setup and configuration
- Provides `GetSoup()` method for BeautifulSoup parsing
- Handles Chrome options (headless mode, extensions, GPU)
- Uses `webdriver_manager` for automatic ChromeDriver management

## Script Purposes

- **`scripts/migrationtrend.py`**: Generates migration trend plots for multiple species
- **`scripts/migrationtrendfun.py`**: Core function `GetSpeciesPlot()` using MigrationScraper → MigrationProcessor pattern
- **`scripts/getobservations.py`**: Scrapes observations using ObservationCollectionScraper → ObservationProcessor pattern
- **`scripts/updateranking.py`**: Updates self-find competition ranking with filtering and point assignment

## Results Directory

All output files are saved to `results/` directory:
- **CSV files** - Scraped data (DataFrames)
- **KML files** - Geographic export
- **TXT files** - Ranking reports
- **PNG files** - Migration plots

The directory is created automatically and is git-ignored.

## Testing Approach

### Unit Tests (Fast - Use Mocks)

**HTML Mocks** (`tests/mocks/*.html`) - For testing scrapers without Selenium:
- `observation_page.html` - Normal observation
- `observation_page_obscured.html` - Obscured GPS coordinates

**CSV Mocks** (`tests/mocks/*.csv`) - For testing processors without scraping:
- `observations_mock.csv` - Sample observation data
- `migration_mock.csv` - Sample migration data

### Integration Tests (Slow - Skipped by Default)

Marked with `@pytest.mark.integration` and skipped unless explicitly run with `pytest -m integration`.

## Important Notes

- **Password Management**: Never commit `passwords/passwords.py`. Use the example file as template.
- **Language Setting**: Scraper sets language to Dutch ('nl') for consistent results
- **Headless Mode**: Chrome headless mode commented out by default in `base.py:21` - uncomment for background execution
- **Module Execution**: Always run scripts as modules (`python -m scripts.scriptname`) to ensure proper imports
- **Output Location**: All results automatically saved to `results/` directory
- **Reprocessing**: Can load saved CSV files and reprocess with different parameters without re-scraping
- **Method Chaining**: Processors support chaining: `processor.filter_selffinds().assign_points().to_kml("output.kml")`
