from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




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
      
      #self.pathdriver = "/home/jelotz/chromedriver"
      self.pathdriver = "/home/jelotz/Documents/prog/chromedriver/chromedriver"
      


   def GetSoup(self):
      self.browser.get(self.Link)
      self.PageSoup = soup(self.browser.page_source, "html.parser")



   def PrintSoup(self):
      print(self.PageSoup.prettify)

   def CreateWebDriver(self):
      self.browser = webdriver.Chrome(executable_path = self.pathdriver, chrome_options = self.chrome_options)

   def CloseWebDriver(self):
      self.browser.quit()


#text_to_be_present_in_element

#EC.element_to_be_clickable((By.CLASS_NAME, "leaflet-clickable")))



# EC.text_to_be_present_in_element((By.CLASS_NAME, "leaflet-clickable"),"test"))

#EC.text_to_be_present_in_element((By.ID, "operations_monitoring_tab_current_ct_fields_no_data"), "No data to display")
