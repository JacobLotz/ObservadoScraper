#!/usr/bin/env python3
"""
Standalone script to verify that observation_257848200.html mock matches
real data from https://waarneming.nl/observation/257848200/

This observation should have "self" in the description, marking it as a self-find.

Usage:
    python tests/verify_mock_257848200.py

Or as a module:
    python -m tests.verify_mock_257848200
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


def verify_mock():
    """Verify that the mock HTML matches real website data"""
    url = "https://waarneming.nl/observation/257848200/"

    print(f"\n{'='*70}")
    print("Mock Verification for Observation 257848200 (Vale Gierzwaluw)")
    print(f"{'='*70}\n")

    print(f"Testing URL: {url}")
    print("\n1. Scraping real website...")

    # Create a real browser instance
    base = ScrapeBase(url)
    base.create_web_driver()

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
                    (By.CSS_SELECTOR, f"button[name='language'][value='{base.lang}']")
                )
            )
            button.click()
            time.sleep(2)  # Wait for language change to take effect
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

        if real_data is None:
            print("   ✗ FAILED: Real scraping returned None")
            print("\n   Possible reasons:")
            print("     - Bot detection prevented access (most likely)")
            print("     - GPS coordinates are obscured on this observation")
            print("     - Website structure changed")
            print("     - Page doesn't exist")
            page_title = base.browser.title if base.browser else "Unknown"
            print(f"\n   Page title received: {page_title}")
            return False

        print("   ✓ Successfully scraped real website")

        print("\n2. Loading mock HTML...")
        # Scrape mock version
        mock_scraper = ObservationScraper(url, Mock())
        mock_soup = load_mock_html("observation_257848200.html")
        mock_scraper.page_soup = mock_soup
        mock_scraper.get_soup = Mock()
        mock_data = mock_scraper.scrape()

        if mock_data is None:
            print("   ✗ FAILED: Mock scraping returned None")
            return False

        print("   ✓ Successfully loaded and parsed mock")

        print("\n3. Comparing fields...")

        # Track mismatches
        mismatches = []

        # Compare key fields
        fields_to_compare = [
            ("name", "Species name"),
            ("year", "Year"),
            ("month", "Month"),
            ("day", "Day"),
            ("time", "Time"),
            ("location_name", "Location"),
            ("latitude", "Latitude"),
            ("longitude", "Longitude"),
        ]

        for field, label in fields_to_compare:
            real_val = real_data.get(field)
            mock_val = mock_data.get(field)

            if real_val == mock_val:
                print(f"   ✓ {label}: {real_val}")
            else:
                print(f"   ✗ {label}: real='{real_val}' vs mock='{mock_val}'")
                mismatches.append((label, real_val, mock_val))

        # Check description exists and contains "self" marker
        real_desc = real_data.get("description", "")
        mock_desc = mock_data.get("description", "")

        if "description" in real_data and "description" in mock_data:
            print(f"   ✓ Description: Both present")

            # Check for self-find marker
            if "self" in real_desc.lower():
                print(f"   ✓ Self-find marker: Found in real description")
            else:
                print(f"   ✗ Self-find marker: NOT found in real description")
                mismatches.append(("Self-find marker in real", False, True))

            if "self" in mock_desc.lower():
                print(f"   ✓ Self-find marker: Found in mock description")
            else:
                print(f"   ✗ Self-find marker: NOT found in mock description")
                mismatches.append(("Self-find marker in mock", True, False))
        else:
            print(
                f"   ✗ Description: Missing in {'real' if 'description' not in real_data else 'mock'}"
            )
            mismatches.append(
                ("Description", "description" in real_data, "description" in mock_data)
            )

        # Summary
        print(f"\n{'-'*70}")
        if mismatches:
            print(f"RESULT: ✗ FAILED - {len(mismatches)} mismatch(es) found")
            print(f"{'-'*70}\n")
            print("Mismatches:")
            for label, real_val, mock_val in mismatches:
                print(f"  • {label}:")
                print(f"      Real: {real_val}")
                print(f"      Mock: {mock_val}")
            return False
        else:
            print("RESULT: ✓ SUCCESS - Mock matches real observation data!")
            print(f"{'-'*70}\n")
            print("Summary:")
            print(f"  Species: {real_data['name']}")
            print(f"  Date: {real_data['datetime']}")
            print(f"  Location: {real_data['location_name']}")
            print(f"  GPS: {real_data['latitude']}, {real_data['longitude']}")
            print(f"  Self-find: YES (contains 'self' marker)")
            print()
            return True

    finally:
        # Clean up browser
        print("\n4. Cleaning up...")
        base.close_web_driver()
        print("   ✓ Browser closed")
        print()


if __name__ == "__main__":
    try:
        success = verify_mock()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
