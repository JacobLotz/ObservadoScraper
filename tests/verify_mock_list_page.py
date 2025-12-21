#!/usr/bin/env python3
"""
Standalone script to verify that observations_list_page.html mock matches
real data from a user's observation list page.

This verifies that observation links can be correctly extracted from the
table-based listing format used by waarneming.nl.

URL: https://waarneming.nl/users/41541/observations/?date_after=2025-11-08&date_before=2025-12-14

Usage:
    python tests/verify_mock_list_page.py

Or as a module:
    python -m tests.verify_mock_list_page
"""

import os
import re
import sys
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.base import ScrapeBase


def load_mock_html(filename):
    """Load mock HTML file and return BeautifulSoup object"""
    test_dir = os.path.dirname(__file__)
    mock_file = os.path.join(test_dir, "mocks", filename)
    with open(mock_file, "r", encoding="utf-8") as f:
        html = f.read()
    return BeautifulSoup(html, "html.parser")


def extract_observation_links(soup):
    """Extract observation links using the same pattern as scraper"""
    links = []
    for link in soup.findAll("a", attrs={"href": re.compile("^/observation/")}):
        links.append(link.get("href"))
    return links


def verify_list_mock():
    """Verify that the observations list mock matches real website data"""
    url = "https://waarneming.nl/users/41541/observations/?date_after=2025-11-08&date_before=2025-12-14&species_group=&rarity=&search=&advanced=on&species=&sex=&month=&country_division=&life_stage=&activity=&method=&validation_status="

    print(f"\n{'='*70}")
    print("Mock Verification for Observations List Page")
    print(f"{'='*70}\n")

    print(f"Testing URL: {url}")
    print("(user 41541 observations from 2025-11-08 to 2025-12-14)\n")

    print("1. Scraping real website...")

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
            time.sleep(2)
            print("   ✓ Language set to Dutch")
        except Exception as e:
            print(f"   ⚠ WARNING: Could not set language: {e}")
            print("     Continuing anyway...")

        # Navigate to the observations list page
        print("   • Navigating to observations list URL...")
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
            page_source = base.browser.page_source

        # Parse the real page
        print("   • Extracting observation links from real page...")
        real_soup = BeautifulSoup(page_source, "html.parser")
        real_links = extract_observation_links(real_soup)

        if not real_links:
            print("   ✗ FAILED: No observation links found on real page")
            print("     This might be due to bot detection or page structure change")
            return False

        print(f"   ✓ Found {len(real_links)} observation link(s) on real page")

    finally:
        # Clean up browser
        base.close_web_driver()

    print("\n2. Loading mock HTML...")
    mock_soup = load_mock_html("observations_list_page.html")
    mock_links = extract_observation_links(mock_soup)
    print(f"   ✓ Found {len(mock_links)} observation link(s) in mock")

    print("\n3. Comparing observation links...")

    checks = []

    # Expected links from the mock (first 5 observations)
    expected_links = [
        "/observation/382543115/",
        "/observation/382543112/",
        "/observation/382543109/",
        "/observation/382543107/",
        "/observation/381544968/",
    ]

    # Check if mock contains expected links
    if set(expected_links).issubset(set(mock_links)):
        print(f"   ✓ Mock contains all expected links")
        checks.append(True)
    else:
        print(f"   ✗ Mock missing some expected links")
        missing = set(expected_links) - set(mock_links)
        print(f"     Missing: {missing}")
        checks.append(False)

    # Check if real page contains the first few expected links
    # (Real page may have more observations than mock)
    found_in_real = [link for link in expected_links if link in real_links]
    if len(found_in_real) >= 3:  # Allow some flexibility
        print(
            f"   ✓ Real page contains {len(found_in_real)}/{len(expected_links)} expected observations"
        )
        checks.append(True)
    else:
        print(
            f"   ⚠ Real page only contains {len(found_in_real)}/{len(expected_links)} expected observations"
        )
        print(f"     This may indicate the observations have changed on the website")
        checks.append(False)

    print("\n4. Checking table structure...")

    # Check mock has table structure
    table = mock_soup.find("table", {"class": "table"})
    if table:
        print("   ✓ Mock has table structure")
        checks.append(True)

        # Check table has rows
        rows = table.find_all("tr")
        if len(rows) > 1:  # Header + data rows
            print(f"   ✓ Mock table has {len(rows)-1} data row(s)")
            checks.append(True)
        else:
            print("   ✗ Mock table has no data rows")
            checks.append(False)

        # Check rows have species names
        species_names = mock_soup.find_all("span", {"class": "species-common-name"})
        if species_names:
            print(f"   ✓ Mock has {len(species_names)} species name(s):")
            for name in species_names[:3]:  # Show first 3
                print(f"      • {name.text}")
            checks.append(True)
        else:
            print("   ✗ Mock missing species names")
            checks.append(False)
    else:
        print("   ✗ Mock missing table structure")
        checks.append(False)

    # Summary
    print(f"\n{'-'*70}")
    if all(checks):
        print("RESULT: ✓ SUCCESS - Observations list mock is valid!")
        print(f"{'-'*70}\n")
        print("Summary:")
        print(f"  • Mock contains {len(mock_links)} observation links")
        print(f"  • Real page contains {len(real_links)} observation links")
        print("  • Mock structure validates correctly")
        print("  • This validates ObservationCollectionScraper link extraction")
        print()
        return True
    else:
        print(f"RESULT: ✗ FAILED - {len([c for c in checks if not c])} check(s) failed")
        print(f"{'-'*70}\n")
        return False


if __name__ == "__main__":
    try:
        success = verify_list_mock()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
