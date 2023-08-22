from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Base class containing methods to get soup and set parameters.
class ScrapeBase:
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()

   def SetParam(self):
      self.Wait = 0
      self.chrome_options = Options()
      self.chrome_options.add_argument("--disable-extensions")
      self.chrome_options.add_argument("--disable-gpu")
      self.chrome_options.add_argument("--no-sandbox") # linux only
      self.chrome_options.add_argument("--headless")
      #self.chrome_options.page_load_strategy = 'eager'    

   def GetSoup(self):
      self.browser.get(self.Link)
      self.PageSoup = soup(self.browser.page_source, "html.parser")

   def PrintSoup(self):
      print(self.PageSoup.prettify)

   def CreateWebDriver(self):
      self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

   def CloseWebDriver(self):
      self.browser.quit()
