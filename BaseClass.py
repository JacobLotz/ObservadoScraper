from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup




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
      #self.pathdriver = "/home/jelotz/chromedriver"
      self.pathdriver = "/data/localhome/jelotz/Documents/WebDriver/chromedriver"




   
   def GetSoup(self):
      self.browser.get(self.Link)
      self.PageSoup = soup(self.browser.page_source, "html.parser")

   def PrintSoup(self):
      print(self.PageSoup)

