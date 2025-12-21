# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ObservadoScraper is a Python-based web scraper for waarneming.nl (Dutch nature observation platform). It scrapes species observations, migration trends, and competition rankings, outputting data to KML files and text reports.

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

Use the Makefile for common tasks:
```bash
# Run tests
make test

# Scrape migration trend data
make migtrend

# Update self-find ranking
make ranking

# Get observation data
make observations

# Clean cache
make clean
```

Or run scripts directly as modules:
```bash
python -m scripts.migrationtrend
python -m scripts.updateranking
python -m scripts.getobservations
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_obs.py

# With options (as used in CI)
pytest tests --maxfail=1 --disable-warnings -q
```

**CI Setup**: GitHub Actions workflow (`.github/workflows/python-tests.yml`) mocks passwords for CI using `tests/mocks/passwords.py`. For local testing, create `passwords/passwords.py` based on `passwords/passwords-example.py`.

## Architecture

### Class Hierarchy

**Base Class**: `classes/base.py:ScrapeBase`
- Manages Selenium WebDriver setup and configuration
- Provides `GetSoup()` method for BeautifulSoup parsing
- Handles Chrome options (headless mode, extensions, GPU)
- Uses `webdriver_manager` for automatic ChromeDriver management

**Core Classes**:

1. **`classes/obs.py:Observation`** - Individual observation data
   - Extracts species name, date/time, location, GPS coordinates from observation pages
   - Skips obscured GPS data
   - Methods: `GetData()`, `WriteKMLLine()`, `CheckSelffind()`
   - Checks for "self-find" markers ("Self", "self", "qwerty", "Qwerty") in descriptions

2. **`classes/obscol.py:ObsCollection`** - Collection of observations
   - Scrapes multiple observation pages with pagination
   - Two main workflows:
     - `StartScrapingProcess()`: Scrapes observations and outputs to KML
     - `StartUpdateSelffindRanking()`: Updates competition ranking from self-finds
   - Handles login via `LogIn()` and language setting via `SetLang()`
   - Imports point values from `data/points.json` for ranking calculations

3. **`classes/mig.py:MigClass`** - Migration trend data
   - Scrapes map grid data from Leaflet-based maps
   - Uses explicit waits for map tiles, SVG overlays, and grid cells to load
   - Extracts number of observation squares from map legend

### Script Purposes

- **`scripts/migrationtrend.py`**: Generates migration trend plots for multiple species over multiple years
- **`scripts/migrationtrendfun.py`**: Core function `GetSpeciesPlot()` that scrapes grid square counts across date ranges and plots trends
- **`scripts/getobservations.py`**: Scrapes observations for specific species/date ranges and outputs KML files
- **`scripts/updateranking.py`**: Scrapes observations for competition participants, identifies self-finds, calculates points from `data/points.json`, and generates `results.txt` ranking

### Data Flow

1. Scripts create class instances with waarneming.nl URLs
2. `ScrapeBase.CreateWebDriver()` initializes Chrome browser
3. `GetSoup()` loads pages and parses HTML with BeautifulSoup
4. Child classes extract specific data (observations, migration data)
5. Output to KML files (via simplekml) or text files

## Important Notes

- **Password Management**: Never commit `passwords/passwords.py`. Use the example file as template. CI uses mocked passwords.
- **Language Setting**: `obscol.py:SetLang()` sets language to Dutch ('nl') for consistent scraping
- **Headless Mode**: Chrome headless mode is commented out by default in `base.py:21` - uncomment for background execution
- **Wait Times**: `self.Wait` parameter controls delay between requests (default 0)
- **Module Execution**: Always run scripts as modules (`python -m scripts.scriptname`) to ensure proper imports via `classes/__init__.py`
