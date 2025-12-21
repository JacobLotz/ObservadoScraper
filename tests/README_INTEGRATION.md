# Integration Testing

This directory contains standalone integration verification scripts that validate mock HTML files against real website data or structural correctness.

## Why Not Pytest?

The waarneming.nl website uses bot detection (likely Cloudflare) that:
1. Shows a "checking your browser" interstitial page
2. Blocks automated requests from robots and pytest test runners
3. May require CAPTCHA solving in some cases

Therefore, integration tests must be run as standalone Python scripts rather than pytest tests.

## Mock Verification Scripts

There are **4 verification scripts** for validating the HTML mocks (all using real URLs):

### 1. Real Website Verification (Live Scraping)

These scripts scrape the actual waarneming.nl website and compare against mocks:

#### `verify_mock_382543115.py` - Gewone Zeehond

Verifies `mocks/observation_page.html` against https://waarneming.nl/observation/382543115/

**Usage:**
```bash
python tests/verify_mock_382543115.py
# or: python -m tests.verify_mock_382543115
```

#### `verify_mock_257848200.py` - Vale Gierzwaluw (Self-find)

Verifies `mocks/observation_257848200.html` against https://waarneming.nl/observation/257848200/

This observation contains a "self" marker in the description for self-find detection.

**Usage:**
```bash
python tests/verify_mock_257848200.py
# or: python -m tests.verify_mock_257848200
```

#### `verify_mock_obscured.py` - Wolf (Obscured GPS)

Verifies `mocks/observation_373437223.html` against https://waarneming.nl/observation/373437223/

This observation is a Wolf (Canis lupus) with obscured GPS coordinates for species protection. Tests that the scraper returns `None` when GPS data is missing/obscured.

**Usage:**
```bash
python tests/verify_mock_obscured.py
# or: python -m tests.verify_mock_obscured
```

#### `verify_mock_list_page.py` - Observations List

Verifies `mocks/observations_list_page.html` against a real user observations list page.

URL: https://waarneming.nl/users/41541/observations/?date_after=2025-11-08&date_before=2025-12-14

Tests that observation links can be extracted from table-based list pages.

**Usage:**
```bash
python tests/verify_mock_list_page.py
# or: python -m tests.verify_mock_list_page
```

### 2. Legacy Synthetic Mocks

#### `observation_page_obscured.html` - Havik (Synthetic)

Legacy synthetic mock for obscured observations (no real URL). Still used in unit tests but has been superseded by the real Wolf observation mock (`observation_373437223.html`).

## Quick Test All Mocks

### Using Make (Recommended)

```bash
# Run all integration tests
make test-integration

# Run all tests (unit + integration)
make test-all
```

### Manual Execution

Run all verification scripts individually:

```bash
# All tests require live scraping (slow, requires internet, may hit bot detection)
python tests/verify_mock_382543115.py
python tests/verify_mock_257848200.py
python tests/verify_mock_obscured.py
python tests/verify_mock_list_page.py
```

## How Real Website Verification Works

All verification scripts scrape the real website and compare against mocks:

1. **Set language to Dutch (NL)** - Required for consistent field extraction
2. **Scrape the real website** using Selenium WebDriver
3. **Load the mock HTML** from `tests/mocks/`
4. **Parse both** using the same parsing logic
5. **Compare behavior**:
   - **Normal observations** (`verify_mock_382543115.py`): Compare all fields (species, date, location, GPS, description)
   - **Obscured observations** (`verify_mock_obscured.py`): Verify both return `None` (consistent behavior)
   - **Self-find observations** (`verify_mock_257848200.py`): Verify "self" marker detection
   - **List pages** (`verify_mock_list_page.py`): Verify observation link extraction from tables

## Expected Output Examples

### Successful Real Website Verification

```
======================================================================
Mock Verification for Observation 382543115
======================================================================

Testing URL: https://waarneming.nl/observation/382543115/

1. Scraping real website...
   • Setting language to Dutch (NL)...
   ✓ Language set to Dutch
   • Navigating to observation URL...
   • Waiting for bot detection check to complete...
   • Attempting to scrape observation data...
   ✓ Successfully scraped real website

2. Loading mock HTML...
   ✓ Successfully loaded and parsed mock

3. Comparing fields...
   ✓ Species name: Gewone Zeehond
   ✓ Year: 2025
   ✓ Month: 12
   ✓ Day: 14
   ✓ Time: 13:54
   ✓ Location: Ter Heijde - Zandmotor (ZH)
   ✓ GPS: 52.05759, 4.19180

----------------------------------------------------------------------
RESULT: ✓ SUCCESS - Mock matches real observation data!
----------------------------------------------------------------------
```

### Successful Synthetic Verification

```
======================================================================
Mock Verification for Obscured Observation (Havik)
======================================================================

This is a SYNTHETIC test case - no real URL to compare against.
Purpose: Verify scraper returns None for observations with obscured GPS.

1. Loading mock HTML...
   ✓ Mock loaded

2. Attempting to scrape obscured observation...

3. Verifying behavior...
   ✓ Scraper correctly returned None for obscured GPS

4. Checking mock structure...
   ✓ Species name present: Havik
   ✓ GPS coordinates correctly absent (obscured)

----------------------------------------------------------------------
RESULT: ✓ SUCCESS - Obscured observation mock is valid!
----------------------------------------------------------------------
```

## Exit Codes

All verification scripts use standard exit codes:
- `0` - Success: Mock is valid
- `1` - Failure: Validation failed or error occurred

## When to Run These Scripts

Run verification scripts:
- **After updating mock HTML files** - Ensure mocks still match reality
- **When website structure changes** - Detect breaking changes
- **Before releases** - Validate test fixtures
- **Periodically** - Catch gradual website changes
- **When adding new features** - Verify mocks support new functionality

## Creating New Verification Scripts

### For Real URL Verification

1. Copy `verify_mock_382543115.py` to a new file
2. Update the URL and mock filename
3. Adjust field comparisons if needed
4. Test manually (cannot be automated)

### For Synthetic Verification

1. Copy `verify_mock_obscured.py` or `verify_mock_list_page.py`
2. Update the mock filename and structure checks
3. Define what constitutes a valid mock
4. Can be run automatically (no website access needed)

### Troubleshooting Bot Detection

If the script fails with "Real scraping returned None":

**1. Disable headless mode to see what's happening:**
   - Edit `classes/base.py` line ~21
   - Comment out: `# self.chrome_options.add_argument("--headless")`
   - This lets you see the browser window and any CAPTCHA/bot checks

**2. Wait longer for bot detection:**
   - The script waits 5-15 seconds for bot checks to complete
   - You may need to manually solve a CAPTCHA if one appears
   - Watch the browser window (when not headless) for prompts

**3. Alternative approach - Manual scraping:**
   ```bash
   # Open the page manually in your browser
   # View page source (Ctrl+U or Cmd+U)
   # Copy the HTML
   # Save to tests/mocks/observation_page_NEW.html
   # Compare with existing mock manually
   ```

**4. Use the observation scraper scripts instead:**
   - The main scripts (`updateranking.py`, `getobservations.py`) work better
   - They may have been configured to handle bot detection
   - Run those to verify scraping still works in general

### Understanding the Bot Protection

The website uses a protection service (likely Cloudflare) that:
- Analyzes browser fingerprints
- Checks JavaScript execution
- May show "checking your browser before accessing" pages
- Can detect Selenium/automated browsers

This is why:
- Headless mode often fails (no JavaScript execution visible)
- Pytest specifically gets blocked (known automated test framework)
- Wait times are necessary (for JavaScript checks to complete)
- Sometimes it just won't work in automated mode

### Notes

- **Manual execution required** - Cannot be automated due to bot detection
- **Browser window opens** - You'll see Chrome briefly during scraping
- **May require interaction** - CAPTCHA or manual waiting
- **Requires Selenium** - Ensure ChromeDriver is installed
- **Network dependent** - Requires internet connection
- **Success not guaranteed** - Bot detection may prevent access entirely
