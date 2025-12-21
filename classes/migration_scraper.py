import re

import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base import ScrapeBase
from .utils import get_results_path


class MigrationScraper(ScrapeBase):
    """
    Scrapes migration trend data from waarneming.nl grid maps.
    Returns data as pandas DataFrame.
    """

    def __init__(self, Link):
        self.Link = Link
        self.SetParam()

    def UpdateLink(self, Link):
        """Update the link for scraping a different date range or species"""
        self.Link = Link

    def _get_soup_with_wait(self):
        """
        Load the page and wait for map elements to render.
        """
        self.browser.get(self.Link)
        wait = WebDriverWait(self.browser, 4)

        try:
            # Wait for map tiles to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-tile-loaded")))

            # Wait for the map overlay SVG to be present (the grid data)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-overlay-pane svg"))
            )

            # Wait for the grid cells to be rendered
            wait.until(
                lambda d: len(
                    d.find_elements(
                        By.CSS_SELECTOR,
                        ".leaflet-overlay-pane svg path, .leaflet-overlay-pane svg rect, .leaflet-overlay-pane svg polygon",
                    )
                )
                > 10
            )

            # Wait for the legend panel to appear
            wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".panel-body.map-legend"))
            )

        except Exception as e:
            print("Timed out waiting for map to load.")

        self.PageSoup = soup(self.browser.page_source, "html.parser")

    def _get_n_squares(self):
        """
        Extract the number of grid squares from the map legend.
        Returns 0 if unable to extract.
        """
        try:
            element = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".panel-body.map-legend"))
            )
        except TimeoutException:
            print("Timed out waiting for element, continuing...")
            print(self.Link)
            print("\n.")
            return 0

        text = element.text
        numbers = re.findall(r"\d+", text)

        if len(numbers) >= 2:
            return int(numbers[1])
        else:
            return 0

    def scrape_date_range(self, species_id, start_date, end_date):
        """
        Scrape migration data for a single date range.

        Args:
            species_id: Species ID for waarneming.nl
            start_date: Start date (datetime.date object)
            end_date: End date (datetime.date object)

        Returns:
            Dictionary with date and square count
        """
        link = (
            f"https://waarneming.nl/species/{species_id}/maps/"
            f"?start_date={start_date.strftime('%Y-%m-%d')}"
            f"&end_date={end_date.strftime('%Y-%m-%d')}"
            f"&map_type=grid1k"
        )

        self.UpdateLink(link)
        self._get_soup_with_wait()
        n_squares = self._get_n_squares()

        print(f"{start_date}, {n_squares} squares")

        return {
            "start_date": start_date,
            "end_date": end_date,
            "n_squares": n_squares,
            "species_id": species_id,
        }

    def scrape_date_ranges(self, species_id, date_ranges):
        """
        Scrape migration data for multiple date ranges.

        Args:
            species_id: Species ID for waarneming.nl
            date_ranges: List of (start_date, end_date) tuples

        Returns:
            pandas DataFrame with columns: start_date, end_date, n_squares, species_id
        """
        self.CreateWebDriver()

        results = []
        for start_date, end_date in date_ranges:
            result = self.scrape_date_range(species_id, start_date, end_date)
            results.append(result)

        self.CloseWebDriver()

        df = pd.DataFrame(results)
        return df

    def save(self, df, filename):
        """
        Save DataFrame to CSV file in the results directory.

        Args:
            df: pandas DataFrame to save
            filename: filename (not full path) to save as, e.g., 'migration_data.csv'
        """
        filepath = get_results_path(filename)
        df.to_csv(filepath, index=False)
        print(f"Saved migration data to: {filepath}")

    @staticmethod
    def load(filename):
        """
        Load DataFrame from CSV file from the results directory.

        Args:
            filename: filename (not full path) to load from, e.g., 'migration_data.csv'

        Returns:
            pandas DataFrame
        """
        filepath = get_results_path(filename)
        df = pd.read_csv(filepath)
        # Convert date strings back to datetime
        df["start_date"] = pd.to_datetime(df["start_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])
        print(f"Loaded {len(df)} migration data points from: {filepath}")
        return df
