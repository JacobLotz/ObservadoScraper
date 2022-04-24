from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from BaseClass import *
from Observation import *

class MigClass(ScrapeBase):
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()


   def GetSoupMig(self):
      wait_for_element = 3  # wait timeout in seconds
      self.browser.get(self.Link)

      try:
        WebDriverWait(self.browser, wait_for_element).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "leaflet-clickable")))
      except TimeoutException as e:
        print("Wait Timed out")
        print(e)


      self.PageSoup = soup(self.browser.page_source, "html.parser")

   def GetNSquares(self):
   	return len(str(self.PageSoup.find("svg",{"class": "leaflet-zoom-animated"})).split("<g>")[1:])


