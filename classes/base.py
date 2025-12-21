import time

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ScrapeBase:
    """
    Base class for all web scrapers providing Selenium WebDriver setup and BeautifulSoup parsing.

    Manages browser configuration, page loading, and HTML parsing. All scraper classes
    inherit from this base to get consistent browser behavior and utilities.

    Attributes:
        link: URL to scrape
        wait: Delay in seconds before parsing page (default: 0)
        lang: Language code for website (default: "nl")
        browser: Selenium WebDriver instance
        page_soup: BeautifulSoup object of current page
        chrome_options: Chrome browser configuration options
    """

    def __init__(self, link):
        self.link = link
        self.set_param()

    def set_param(self):
        """
        Initialize scraper parameters and Chrome browser options.

        Sets wait time, language preference, and configures Chrome to run with
        extensions disabled, GPU disabled, and sandbox disabled for Linux compatibility.
        Headless mode is available but commented out by default.
        """
        self.wait = 0
        self.lang = "nl"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        # self.chrome_options.add_argument("--headless")

    def get_soup(self):
        """
        Load the current link in browser and parse HTML with BeautifulSoup.

        Navigates to self.link, waits for self.wait seconds, then parses the page
        source into a BeautifulSoup object stored in self.page_soup.
        """
        self.browser.get(self.link)
        time.sleep(self.wait)
        self.page_soup = soup(self.browser.page_source, "html.parser")

    def print_soup(self):
        """Print the prettified HTML of the current page."""
        print(self.page_soup.prettify)

    def create_web_driver(self):
        """
        Initialize Selenium Chrome WebDriver with configured options.

        Uses webdriver_manager to automatically download and install the correct
        ChromeDriver version. Applies chrome_options set in set_param().
        """
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.chrome_options
        )

    def close_web_driver(self):
        """Close the Selenium WebDriver and quit the browser."""
        self.browser.quit()
