#!/usr/bin/env python3
"""
Standalone script to verify that observation_373437223.html mock matches
real data from https://waarneming.nl/observation/373437223/

This observation is a Wolf (Canis lupus) with obscured GPS coordinates
for species protection. The scraper should return None when GPS is missing.

Usage:
    python tests/verify_mock_obscured.py

Or as a module:
    python -m tests.verify_mock_obscured
"""

import os
import sys
import time
from unittest.mock import Mock

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import ObservationScraper
from classes.base import ScrapeBase


def load_mock_html(filename):
    """Load mock HTML file and return BeautifulSoup object"""
    test_dir = os.path.dirname(__file__)
    mock_file = os.path.join(test_dir, "mocks", filename)
    with open(mock_file, "r", encoding="utf-8") as f:
        html = f.read()
    return BeautifulSoup(html, "html.parser")


def verify_obscured_mock():
    """Verify that the obscured observation mock is correctly handled"""
    url = "https://waarneming.nl/observation/373437223/"

    print(f"\n{'='*70}")
    print("Mock Verification for Obscured Observation 373437223 (Wolf)")
    print(f"{'='*70}\n")

    print(f"Testing URL: {url}")
    print("This observation has obscured GPS coordinates (protected species).\n")

    print("1. Scraping real website...")

    # Create a real browser instance
    base = ScrapeBase(url)
    base.CreateWebDriver()

    try:
        # Set language to Dutch first
        print("   • Setting language to Dutch (NL)...")
        lang_url = "https://waarneming.nl/generic/select-language-modal/"
        base.browser.get(lang_url)

        try:
            # Wait for the language button and click it
            wait = WebDriverWait(base.browser, 10)
            button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"button[name='language'][value='{base.Lang}']")
                )
            )
            button.click()
            time.sleep(2)
            print("   ✓ Language set to Dutch")
        except Exception as e:
            print(f"   ⚠ WARNING: Could not set language: {e}")
            print("     Continuing anyway...")

        # Navigate to the observation page
        print("   • Navigating to observation URL...")
        base.browser.get(url)

        # Wait for bot detection to complete
        print("   • Waiting for bot detection check to complete...")
        time.sleep(5)

        # Check if we got past bot detection
        page_source = base.browser.page_source
        if "checking your browser" in page_source.lower() or "cloudflare" in page_source.lower():
            print("   ⚠ WARNING: Still on bot detection page")
            print("     Waiting an additional 10 seconds...")
            time.sleep(10)

        # Now try to scrape
        print("   • Attempting to scrape observation data...")
        real_scraper = ObservationScraper(url, base.browser)
        real_data = real_scraper.scrape()

        # For obscured observations, we expect None
        if real_data is None:
            print("   ✓ Real website correctly returned None (GPS obscured)")
            real_returns_none = True
        else:
            print(f"   ⚠ Unexpected: Real website returned data: {real_data}")
            print("     This might mean the observation is no longer obscured,")
            print("     or you are logged in with special access permissions.")
            real_returns_none = False

    finally:
        # Clean up browser
        base.CloseWebDriver()

    print("\n2. Loading mock HTML...")
    # Scrape mock version
    mock_scraper = ObservationScraper(url, Mock())
    mock_soup = load_mock_html("observation_373437223.html")
    mock_scraper.PageSoup = mock_soup
    mock_scraper.GetSoup = Mock()
    mock_data = mock_scraper.scrape()

    if mock_data is None:
        print("   ✓ Mock correctly returns None (GPS coordinates absent)")
        mock_returns_none = True
    else:
        print(f"   ✗ FAILED: Mock should return None but returned: {mock_data}")
        mock_returns_none = False

    print("\n3. Checking mock structure...")

    # Track checks
    checks = []

    # Check species name is present
    species = mock_soup.find("span", {"class": "species-common-name"})
    if species and species.text.strip() == "Wolf":
        print("   ✓ Species name present: Wolf")
        checks.append(True)
    else:
        print("   ✗ Species name missing or incorrect")
        checks.append(False)

    # Check observation details table exists
    table = mock_soup.find("table", {"id": "observation_details"})
    if table:
        print("   ✓ Observation details table present")
        checks.append(True)
    else:
        print("   ✗ Observation details table missing")
        checks.append(False)

    # Check GPS coordinates are indeed missing
    gps = mock_soup.find("span", {"class": "teramap-coordinates-coords"})
    if gps is None:
        print("   ✓ GPS coordinates correctly absent (obscured)")
        checks.append(True)
    else:
        print("   ✗ GPS coordinates should be absent for obscured observation")
        checks.append(False)

    # Check description mentions obscuration or protection
    desc = mock_soup.find("div", {"class": "goog-trans-section"})
    if desc and ("vervaagd" in desc.text.lower() or "bescherming" in desc.text.lower()):
        print("   ✓ Description mentions obscuration/protection")
        checks.append(True)
    else:
        print("   ✗ Description should mention obscuration/protection")
        checks.append(False)

    print("\n4. Verifying behavior consistency...")

    if real_returns_none and mock_returns_none:
        print("   ✓ Both real and mock return None (consistent)")
        checks.append(True)
    elif not real_returns_none and not mock_returns_none:
        print("   ⚠ Both real and mock return data (observation may not be obscured)")
        checks.append(True)  # Still consistent, just different than expected
    else:
        print("   ✗ Inconsistent: real and mock behave differently")
        checks.append(False)

    # Summary
    print(f"\n{'-'*70}")
    if all(checks):
        print("RESULT: ✓ SUCCESS - Obscured observation mock is valid!")
        print(f"{'-'*70}\n")
        print("Summary:")
        print("  • Mock has correct structure")
        print("  • GPS coordinates are absent (as expected for Wolf)")
        print("  • Scraper correctly returns None")
        print("  • This validates handling of protected/obscured species")
        print()
        return True
    else:
        print(f"RESULT: ✗ FAILED - {len([c for c in checks if not c])} check(s) failed")
        print(f"{'-'*70}\n")
        return False


if __name__ == "__main__":
    try:
        success = verify_obscured_mock()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
