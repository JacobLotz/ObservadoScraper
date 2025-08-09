from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import time

# Base class containing methods to get soup and set parameters.
class ScrapeBase:
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()

   def SetParam(self):
      self.Wait = 0
      self.Lang = 'nl'
      self.chrome_options = Options()
      self.chrome_options.add_argument("--disable-extensions")
      self.chrome_options.add_argument("--disable-gpu")
      self.chrome_options.add_argument("--no-sandbox") # linux only
      #self.chrome_options.add_argument("--headless")

   def GetSoup(self):
      self.browser.get(self.Link)
      time.sleep(self.Wait)
      self.PageSoup = soup(self.browser.page_source, "html.parser")

   def PrintSoup(self):
      print(self.PageSoup.prettify)

   def CreateWebDriver(self):
      self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

   def CloseWebDriver(self):
      self.browser.quit()
