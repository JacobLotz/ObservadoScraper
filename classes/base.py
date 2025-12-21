import time

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Base class containing methods to get soup and set parameters.
class ScrapeBase:
    def __init__(self, link):
        self.link = link
        self.set_param()

    def set_param(self):
        self.wait = 0
        self.lang = "nl"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        # self.chrome_options.add_argument("--headless")

    def get_soup(self):
        self.browser.get(self.link)
        time.sleep(self.wait)
        self.page_soup = soup(self.browser.page_source, "html.parser")

    def print_soup(self):
        print(self.page_soup.prettify)

    def create_web_driver(self):
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.chrome_options
        )

    def close_web_driver(self):
        self.browser.quit()
