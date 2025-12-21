# ObservadoScraper

A Python-based web scraper for [waarneming.nl](https://waarneming.nl), the Dutch nature observation platform. Scrapes species observations, migration trends, and competition rankings, outputting data to KML files, CSV files, and text reports.

## Features

- **Observation Scraping**: Extract detailed observation data from waarneming.nl pages
- **Migration Trends**: Analyze and visualize species migration patterns over time
- **Self-Find Competition**: Track and rank self-found rare species observations
- **Data Export**: Export to KML (Google Earth), CSV, and formatted text reports
- **Modular Architecture**: Separate data gathering (scrapers) from processing (processors)
- **Comprehensive Testing**: 38 unit tests + 4 integration verification scripts

## Architecture

**Workflow**: Scrape → Save CSV → Load CSV → Process → Export

- **Scrapers** (data gathering): ObservationScraper, ObservationCollectionScraper, MigrationScraper
- **Processors** (data processing): ObservationProcessor, MigrationProcessor
- **Intermediate format**: pandas DataFrames

## Installation

### Prerequisites

- Python 3.9+
- Conda package manager
- Google Chrome browser (for Selenium)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd ObservadoScraper

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate observadoscraper

# Set up passwords (for login features)
cp passwords/passwords-example.py passwords/passwords.py
# Edit passwords/passwords.py with your credentials
```

## Usage

### Quick Start with Makefile

```bash
# Run unit tests
make test

# Format code
make style

# Update self-find ranking
make ranking

# Generate migration trend plots
make migtrend

# Scrape observations
make observations
```

### Running Scripts Directly

Always run scripts as modules to ensure proper imports:

```bash
# Scrape observations
python -m scripts.getobservations

# Update self-find competition ranking
python -m scripts.updateranking

# Generate migration trend plots
python -m scripts.migrationtrend
```

### Programmatic Usage

```python
from classes import ObservationCollectionScraper, ObservationProcessor

# 1. Scrape data
link = "https://waarneming.nl/species/133/observations/?..."
scraper = ObservationCollectionScraper(link)
df = scraper.scrape()

# 2. Save to CSV
scraper.save(df, "observations.csv")

# 3. Process data (can be done later, separately)
processor = ObservationProcessor(df)
processor.filter_selffinds().assign_points().to_kml("selffinds.kml")
```

## Testing

### Unit Tests (Fast)

```bash
make test              # Run all 38 unit tests
pytest -v              # Same, using pytest directly
```

All unit tests use HTML and CSV mocks - no internet connection required.

### Integration Tests (Slow, Requires Internet)

```bash
make test-integration  # Run all 4 integration verification scripts
make test-all          # Run unit + integration tests
```

Integration tests validate mocks against real waarneming.nl pages. May be blocked by bot detection.

## Code Style

The project enforces consistent code style with automated tools:

```bash
make style        # Auto-format with black & isort
make style-check  # Verify compliance
make lint         # Run flake8 linter
```

**Style rules**:
- Line length: 100 characters
- Naming: snake_case enforced (methods, variables, parameters)
- Import ordering: stdlib → third-party → first-party
- Black formatting with double quotes

## Output

All output files are saved to the `results/` directory (auto-created, git-ignored):

- **CSV files**: Scraped observation and migration data
- **KML files**: Geographic data for Google Earth
- **TXT files**: Competition ranking reports
- **PNG files**: Migration trend plots

## Project Structure

```
ObservadoScraper/
├── classes/              # Core scraper and processor classes
│   ├── base.py          # Base class with Selenium setup
│   ├── observation_scraper.py
│   ├── observation_collection_scraper.py
│   ├── observation_processor.py
│   ├── migration_scraper.py
│   ├── migration_processor.py
│   └── utils.py         # Utility functions
├── scripts/             # Executable scripts
│   ├── getobservations.py
│   ├── updateranking.py
│   └── migrationtrend.py
├── tests/               # Unit tests and integration tests
│   ├── mocks/          # HTML and CSV test fixtures
│   └── verify_*.py     # Integration verification scripts
├── data/               # Static data (points.json)
├── passwords/          # Credentials (git-ignored)
├── results/            # Output directory (git-ignored)
├── environment.yml     # Conda environment specification
├── Makefile           # Common tasks
└── CLAUDE.md          # Developer documentation
```

## Configuration

- **ChromeDriver**: Automatically managed by `webdriver_manager` (no manual setup needed)
- **Language**: Scraper sets language to Dutch (nl) for consistent results
- **Headless mode**: Commented out in `classes/base.py:23` - uncomment for background execution
- **Passwords**: Store in `passwords/passwords.py` (see `passwords-example.py`)

## Known Limitations

- **Bot Detection**: waarneming.nl uses Cloudflare protection - integration tests may fail
- **Login Required**: Some features require waarneming.nl account credentials
- **Mock Drift**: Integration tests may fail if observations are edited on the website
- **Language Dependent**: Scraper expects Dutch language settings

## Development

### Running Tests

```bash
make test              # Fast unit tests with mocks
make test-integration  # Slow integration tests (live scraping)
make test-all          # All tests
```

### Code Quality

```bash
make style        # Auto-format code
make style-check  # Verify style compliance
make lint         # Run linter only
make clean        # Clean up cache files
```

### Contributing

1. Ensure all tests pass: `make test`
2. Format code: `make style`
3. Verify compliance: `make style-check`
4. Update documentation as needed

## Troubleshooting

### Integration Tests Fail

Integration tests scrape live websites and may fail due to:
- Bot detection (Cloudflare)
- Observations edited on website
- Network issues

**Solution**: Update mocks manually or run scripts directly (non-pytest).

### ImportError

Always run scripts as modules:
```bash
# ✅ Correct
python -m scripts.getobservations

# ❌ Wrong
python scripts/getobservations.py
```

### ChromeDriver Issues

ChromeDriver is managed automatically by `webdriver_manager`. If issues occur:
1. Ensure Chrome browser is installed
2. Check internet connection (for driver download)
3. Try deleting `~/.wdm/` cache directory

## License

See repository for license information.

## Contact

For issues and questions, please use the GitHub issue tracker.
