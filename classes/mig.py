from bs4 import BeautifulSoup as soup
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from classes import *

class MigClass(ScrapeBase):
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()

   def UpdateLink(self, Link):
      self.Link = Link;

   def GetSoupMig(self):
      wait_for_element = 1  # wait timeout in seconds
      self.browser.get(self.Link)
      wait = WebDriverWait(self.browser, 4)
      try:
         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-tile-loaded")))

         # Wait for the map overlay SVG to be present (the grid data)
         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-overlay-pane svg")))

         # Wait for the grid cells to be rendered — usually 'path', 'rect', or 'polygon'
         wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".leaflet-overlay-pane svg path, .leaflet-overlay-pane svg rect, .leaflet-overlay-pane svg polygon")) > 10)

         # Optionally: wait for the legend panel to appear
         wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".panel-body.map-legend")))

      except Exception as e:
         print("Timed out waiting for map to load.")

      self.PageSoup = soup(self.browser.page_source, "html.parser")

   def GetNSquares(self):
      element = self.browser.find_element("css selector", ".panel-body.map-legend")
      text = element.text
      
      numbers = re.findall(r'\d+', text)


      if len(numbers) >= 2:
         return int(numbers[1])
      else:
         return 0



