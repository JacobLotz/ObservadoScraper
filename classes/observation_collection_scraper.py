import re
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import ScrapeBase
from .observation_scraper import ObservationScraper
from .utils import get_results_path

# import password from external file
from passwords.passwords import username_in, password_in


class ObservationCollectionScraper(ScrapeBase):
    """
    Scrapes multiple observations from waarneming.nl overview pages.
    Returns a pandas DataFrame with all observation data.
    """

    def __init__(self, Link):
        super().__init__(Link)

    def LogIn(self):
        """Log into old website"""
        url = 'https://waarneming.nl/accounts/login/?next=/'
        self.browser.get(url)
        user_name = self.browser.find_element("name", "login")
        user_name.send_keys(username_in)
        password = self.browser.find_element("name", 'password')
        password.send_keys(password_in)
        password.send_keys(Keys.RETURN)

    def SetLang(self):
        """Set language for new website"""
        url = "https://waarneming.nl/generic/select-language-modal/"
        self.browser.get(url)

        # Wait for the language button and click it directly
        wait = WebDriverWait(self.browser, 10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[name='language'][value='{self.Lang}']")))
        button.click()

    def _get_observation_links(self):
        """
        Collects all observation links from paginated overview pages.
        Returns a list of observation URLs.
        """
        obs_links = []
        base_link = self.Link[0:-1]
        page = 0

        print('Starting to retrieve links from overview pages')

        # Get links from page to observations
        is_end = False
        while not is_end:
            time.sleep(self.Wait)
            page += 1

            print(f'Currently in page {page}\r', end="")
            self.Link = base_link + str(page)
            self.GetSoup()

            for link in self.PageSoup.findAll('a', attrs={'href': re.compile("^/observation/")}):
                obs_links.append(link.get('href'))

            # Check if on last page, if so: end loop
            try:
                last_page = self.PageSoup.findAll('li', attrs={'last'})[0].find('a').get('href')
            except:  # Exception for one page
                last_page = None

            if last_page is None:
                is_end = True
                print(f'Currently in page {page}')
                print(f"Found {page} pages of observations having a total of {len(obs_links)} observations.\n")

        return obs_links

    def _get_observation_links_filtered(self, species_filter):
        """
        Collects observation links filtered by species names.
        Used for self-find ranking updates.

        Args:
            species_filter: Set or list of species names to filter for

        Returns a list of observation URLs.
        """
        obs_links = []
        base_link = self.Link[0:-1]
        page = 0

        print('Starting to retrieve links from overview pages')

        is_end = False
        while not is_end:
            time.sleep(self.Wait)
            page += 1

            print(f'Currently in page {page}\r', end="")
            self.Link = base_link + str(page)
            self.GetSoup()

            links = []
            for link in self.PageSoup.findAll('a', attrs={'href': re.compile("^/observation/")}):
                links.append(link.get('href'))

            species = self.PageSoup.findAll("span", {"class": ["species-common-name"]})
            potential_indices = []

            i = 0
            for sp in species:
                test_species = sp.get_text()
                if test_species in species_filter:
                    potential_indices.append(i)
                i += 1

            # Get potential links
            for i in potential_indices:
                obs_links.append(links[i])

            # Check if on last page
            try:
                last_page = self.PageSoup.findAll('li', attrs={'last'})[0].find('a').get('href')
            except:
                last_page = None

            if last_page is None:
                is_end = True
                print(f'Currently in page {page}')
                print(f"Found {page} pages of observations having a total of {len(obs_links)} observations.\n")

        return obs_links

    def scrape(self, species_filter=None):
        """
        Main scraping method. Collects observation links and scrapes each observation.

        Args:
            species_filter: Optional set/list of species names to filter for

        Returns:
            pandas DataFrame with observation data
        """
        print('\n-------------------------------------')
        print('Starting to scrape observation collection')

        # Get links to relevant observations
        self.CreateWebDriver()
        self.SetLang()

        if species_filter:
            obs_links = self._get_observation_links_filtered(species_filter)
        else:
            obs_links = self._get_observation_links()

        # Scrape each observation
        print('Starting extraction of data from observations')
        observations = []

        for i, link in enumerate(obs_links):
            time.sleep(self.Wait)

            progress = int((i + 1) / len(obs_links) * 100)
            if progress < 100:
                print(f'Scraping pages [{progress}%]\r', end="")
            else:
                print('Scraping pages [100%]')

            full_link = 'https://waarneming.nl' + link
            obs_scraper = ObservationScraper(full_link, self.browser)
            obs_data = obs_scraper.scrape()

            if obs_data:  # Skip if no GPS data
                observations.append(obs_data)

        self.CloseWebDriver()

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
