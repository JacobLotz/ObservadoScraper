# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ObservadoScraper is a Python-based web scraper for waarneming.nl (Dutch nature observation platform). It scrapes species observations, migration trends, and competition rankings, outputting data to KML files and text reports.

**Architecture**: Modular design separating data gathering (scrapers) from data processing (processors), with pandas DataFrames as the intermediate format.

## TODO - Cleanup Tasks

### Medium Priority
- [ ] **Replace print with logging** - Replace ~29 print statements in classes/ with Python logging module
- [ ] **Extract magic numbers** - Move hardcoded values (timeouts, sleep values) to named constants

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
make test              # Run unit tests
make test-integration  # Run integration tests (slow)
make test-all          # Run all tests
make style             # Format code with black & isort
make style-check       # Check code style compliance
make lint              # Run flake8 linter
make migtrend          # Generate migration trend plots
make ranking           # Update self-find ranking
make observations      # Scrape observations
make clean             # Clean up cache files
```

**Output Location**: All output files (CSV, KML, TXT, PNG) are saved to the `results/` directory, which is created automatically and git-ignored.

## Testing

### Unit Tests (Fast, No Internet)

```bash
# Run all unit tests (38 tests, fast with mocks)
make test
# or: make test-unit
# or: pytest

# Run specific test categories
pytest tests/test_observation_processor.py  # Processor tests with CSV mocks
pytest tests/test_observation_scraper.py    # Scraper tests with HTML mocks
```

**Test Coverage**: 38 passing tests using HTML and CSV mocks. No live scraping needed for unit tests.

### Integration Tests (Slow, Requires Internet)

```bash
# Run all integration tests (validates mocks against real website)
make test-integration

# Or run individual integration tests
python tests/verify_mock_382543115.py      # Normal observation
python tests/verify_mock_257848200.py      # Self-find observation
python tests/verify_mock_obscured.py       # Obscured GPS observation
python tests/verify_mock_list_page.py      # Observations list page
```

**Integration Coverage**: 4 verification scripts that scrape real waarneming.nl pages to validate mocks. See `tests/README_INTEGRATION.md` for details.

**Important**: Integration tests may fail if observations on waarneming.nl are edited. Observations can be modified by their observers (e.g., removing time values, changing descriptions). When integration tests fail:

1. Run the failing test individually to see the mismatch
2. Update the corresponding mock HTML file in `tests/mocks/`
3. Update the corresponding unit test assertions in `tests/test_observation_scraper.py`
4. Verify all unit tests still pass: `make test`

Example: Observations 382543115 and 257848200 had their time values removed from the website in December 2024, requiring mock updates.

### Run All Tests

```bash
# Run both unit and integration tests
make test-all
```

**CI Setup**: GitHub Actions workflow (`.github/workflows/python-tests.yml`) mocks passwords using `tests/mocks/passwords.py`. For local testing, create `passwords/passwords.py` based on `passwords/passwords-example.py`.

**Note**: Only run unit tests in CI/automated environments. Integration tests require manual execution due to bot detection and potential observation changes on the website.

## Code Style

The project uses automated code formatting and linting tools to maintain consistent code style:

### Tools

- **black** - Automatic code formatter (line length: 100)
- **isort** - Import statement organizer
- **flake8** - Linter for code quality and style checking

### Configuration Files

- `pyproject.toml` - Black and isort settings
- `.flake8` - Flake8 linting rules

### Usage

```bash
# Check code style compliance (no changes)
make style-check

# Automatically fix code style issues
make style
# or: make style-fix

# Run only linter (no automatic fixes)
make lint
```

### Running Style Tools

**Before committing code**, run:
```bash
make style        # Auto-format code with black & isort
make style-check  # Verify compliance
```

### Style Rules

- **Line length**: 100 characters max
- **Import ordering**: Standard library → Third-party → First-party (classes, scripts, passwords)
- **String quotes**: Double quotes preferred by black
- **Trailing commas**: Required in multi-line structures
- **Naming conventions**: **snake_case enforced**
  - Functions: `get_soup()`, `create_web_driver()`
  - Variables: `page_soup`, `obs_links`, `base_link`
  - Parameters: `link`, `species_filter`, `date_ranges`
  - Classes: `CapWords` (ScrapeBase, ObservationScraper)

The formatters run on `classes/`, `scripts/`, and `tests/` directories.

**Important**: All Python code uses snake_case naming (enforced by pep8-naming plugin). This includes:
- Method names: `set_param()` not `SetParam()`
- Attribute names: `self.link` not `self.Link`
- Function names: `get_month_end()` not `GetMonthEnd()`

## Architecture

### Modular Design

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

### Base Class

**`classes/base.py:ScrapeBase`**
- Manages Selenium WebDriver setup and configuration
- Provides `get_soup()` method for BeautifulSoup parsing
- Handles Chrome options (headless mode, extensions, GPU)
- Uses `webdriver_manager` for automatic ChromeDriver management

## Script Purposes

- **`scripts/migrationtrend.py`**: Generates migration trend plots for multiple species
- **`scripts/migrationtrendfun.py`**: Core function `get_species_plot()` using MigrationScraper → MigrationProcessor pattern
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
- `observation_page.html` - Normal observation (from real observation 382543115)
- `observation_257848200.html` - Vale Gierzwaluw self-find observation (real observation)
- `observation_373437223.html` - Wolf with obscured GPS (real observation)
- `observations_list_page.html` - User observations list (from real list page)
- `observation_page_obscured.html` - Havik obscured GPS (legacy synthetic mock)

**CSV Mocks** (`tests/mocks/*.csv`) - For testing processors without scraping:
- `observations_mock.csv` - Sample observation data
- `migration_mock.csv` - Sample migration data

**Mock Maintenance**: Mocks based on real observations may become outdated when observers edit their observations on waarneming.nl. Integration tests detect these changes. Update mocks when:
- Times are added/removed from observations
- Descriptions are modified
- GPS coordinates are obscured/revealed
- Any other field changes on the website

## Important Notes

- **Password Management**: Never commit `passwords/passwords.py`. Use the example file as template.
- **Language Setting**: Scraper sets language to Dutch ('nl') for consistent results via `set_lang()` method
- **Headless Mode**: Chrome headless mode commented out by default in `base.py:23` - uncomment for background execution
- **Module Execution**: Always run scripts as modules (`python -m scripts.scriptname`) to ensure proper imports
- **Output Location**: All results automatically saved to `results/` directory
- **Reprocessing**: Can load saved CSV files and reprocess with different parameters without re-scraping
- **Method Chaining**: Processors support chaining: `processor.filter_selffinds().assign_points().to_kml("output.kml")`
- **Bot Detection**: The website uses Cloudflare protection. Integration tests handle this with wait times and language setting, but may still fail occasionally. Manual execution (not pytest) works better.
- **Mock Drift**: HTML mocks based on real observations can become outdated when observations are edited on the website. Run integration tests periodically to detect and fix drift.
