import re
import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# import password from external file
from passwords.passwords import password_in, username_in

from .base import ScrapeBase
from .observation_scraper import ObservationScraper
from .utils import get_results_path


class ObservationCollectionScraper(ScrapeBase):
    """
    Scrapes multiple observations from waarneming.nl overview pages.
    Returns a pandas DataFrame with all observation data.
    """

    def __init__(self, link):
        super().__init__(link)

    def log_in(self):
        """Log into old website"""
        url = "https://waarneming.nl/accounts/login/?next=/"
        self.browser.get(url)
        user_name = self.browser.find_element("name", "login")
        user_name.send_keys(username_in)
        password = self.browser.find_element("name", "password")
        password.send_keys(password_in)
        password.send_keys(Keys.RETURN)

    def set_lang(self):
        """Set language for new website"""
        url = "https://waarneming.nl/generic/select-language-modal/"
        self.browser.get(url)

        # Wait for the language button and click it directly
        wait = WebDriverWait(self.browser, 10)
        button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"button[name='language'][value='{self.lang}']")
            )
        )
        button.click()

    def _paginate_and_collect(self, link_extractor):
        """
        Common pagination logic for collecting observation links.

        Args:
            link_extractor: Callable that takes the current page soup and returns
                          a list of observation links to add from this page

        Returns:
            List of observation URLs collected from all pages
        """
        obs_links = []
        base_link = self.link[0:-1]
        page = 0

        print("Starting to retrieve links from overview pages")

        is_end = False
        while not is_end:
            time.sleep(self.wait)
            page += 1

            print(f"Currently in page {page}\r", end="")
            self.link = base_link + str(page)
            self.get_soup()

            # Extract links from current page using provided function
            page_links = link_extractor(self.page_soup)
            obs_links.extend(page_links)

            # Check if on last page
            try:
                last_page = self.page_soup.findAll("li", attrs={"last"})[0].find("a").get("href")
            except (IndexError, AttributeError, KeyError):  # Exception for one page
                last_page = None

            if last_page is None:
                is_end = True
                print(f"Currently in page {page}")
                print(
                    f"Found {page} pages of observations having a total of {len(obs_links)} observations.\n"
                )

        return obs_links

    def _get_observation_links(self):
        """
        Collects all observation links from paginated overview pages.
        Returns a list of observation URLs.
        """

        def extract_all_links(page_soup):
            """Extract all observation links from page."""
            return [
                link.get("href")
                for link in page_soup.findAll("a", attrs={"href": re.compile("^/observation/")})
            ]

        return self._paginate_and_collect(extract_all_links)

    def _get_observation_links_filtered(self, species_filter):
        """
        Collects observation links filtered by species names.
        Used for self-find ranking updates.

        Args:
            species_filter: Set or list of species names to filter for

        Returns a list of observation URLs.
        """

        def extract_filtered_links(page_soup):
            """Extract observation links filtered by species."""
            links = [
                link.get("href")
                for link in page_soup.findAll("a", attrs={"href": re.compile("^/observation/")})
            ]

            species = page_soup.findAll("span", {"class": ["species-common-name"]})
            filtered_links = []

            for i, sp in enumerate(species):
                if sp.get_text() in species_filter:
                    filtered_links.append(links[i])

            return filtered_links

        return self._paginate_and_collect(extract_filtered_links)

    def scrape(self, species_filter=None):
        """
        Main scraping method. Collects observation links and scrapes each observation.

        Args:
            species_filter: Optional set/list of species names to filter for

        Returns:
            pandas DataFrame with observation data
        """
        print("\n-------------------------------------")
        print("Starting to scrape observation collection")

        # Get links to relevant observations
        self.create_web_driver()
        self.set_lang()

        if species_filter:
            obs_links = self._get_observation_links_filtered(species_filter)
        else:
            obs_links = self._get_observation_links()

        # Scrape each observation
        print("Starting extraction of data from observations")
        observations = []

        for i, link in enumerate(obs_links):
            time.sleep(self.wait)

            progress = int((i + 1) / len(obs_links) * 100)
            if progress < 100:
                print(f"Scraping pages [{progress}%]\r", end="")
            else:
                print("Scraping pages [100%]")

            full_link = "https://waarneming.nl" + link
            obs_scraper = ObservationScraper(full_link, self.browser)
            obs_data = obs_scraper.scrape()

            if obs_data:  # Skip if no GPS data
                observations.append(obs_data)

        self.close_web_driver()

        # Convert to DataFrame
        df = pd.DataFrame(observations)
        print(f"Successfully scraped {len(df)} observations")

        return df

    def save(self, df, filename):
        """
        Save DataFrame to CSV file in the results directory.

        Args:
            df: pandas DataFrame to save
            filename: filename (not full path) to save as, e.g., 'observations.csv'
        """
        filepath = get_results_path(filename)
        df.to_csv(filepath, index=False)
        print(f"Saved data to: {filepath}")

    @staticmethod
    def load(filename):
        """
        Load DataFrame from CSV file from the results directory.

        Args:
            filename: filename (not full path) to load from, e.g., 'observations.csv'

        Returns:
            pandas DataFrame
        """
        filepath = get_results_path(filename)
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} observations from: {filepath}")
        return df
