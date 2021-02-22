from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import simplekml
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


# Base class containing methods to get soup and set parameters.
class ScrapeBase:
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()

   def SetParam(self):
      self.Wait = 0
      self.IfOld = 1




   
   def GetSoup(self):
      #new:
      self.browser.get(self.Link)
      self.PageSoup = soup(self.browser.page_source, "html.parser")
      #soup = BeautifulSoup(browser.page_source, 'lxml')

      #old:
      #uClient = uReq(self.Link)
      #html = uClient.read()
      #uClient.close
      #self.PageSoup = soup(html, "html.parser")
      

   def PrintSoup(self):
      print(self.PageSoup)



# Class inheriting from baseclass which creates a collection of observations and uses 
# the class Observation to get its data. Class can be constructed by giving a link 
# and a name.
class ObsCollection(ScrapeBase):



   def CreateWebDriver(self):
      chrome_options = Options()
      #chrome_options.add_argument("--disable-extensions")
      #chrome_options.add_argument("--disable-gpu")
      #chrome_options.add_argument("--no-sandbox") # linux only
      #chrome_options.add_argument("--headless")
      pathdriver = "/data/localhome/jelotz/Documents/WebDriver/chromedriver"
      self.browser = webdriver.Chrome(executable_path = pathdriver, chrome_options = chrome_options)

   def CloseWebDriver(self):
      self.browser.quit()

   def LogIn(self):
      # Activate Phantom(headless) and deactivate Chrome to not load browser
      #browser = webdriver.PhantomJS()

      url = 'https://waarneming.nl/accounts/login/?next=/'
      self.browser.get(url)
      user_name = self.browser.find_element_by_name("login")
      user_name.send_keys("lotzzzz")
      password = self.browser.find_element_by_name('password')
      password.send_keys("jacoblotz")
      password.send_keys(Keys.RETURN)

   def LogInOld(self):
      # Activate Phantom(headless) and deactivate Chrome to not load browser
      #browser = webdriver.PhantomJS()

      url = 'https://old.waarneming.nl/user/login'
      self.browser.get(url)
      user_name = self.browser.find_element_by_name("user")
      user_name.send_keys("lotzzzz")
      password = self.browser.find_element_by_name('password')
      password.send_keys("jacoblotz")
      password.send_keys(Keys.RETURN)


   def SetLang(self):
      url = "https://waarneming.nl/generic/select-language-modal/"
      self.browser.get(url)
      button = self.browser.find_elements_by_name("language")
      button = button[35]
      button.click()
      


   def SetName(self, Name):
      self.Name = Name
      

   # Method for performing the whole scraping process after initialization
   def StartScrapingProcess(self):
      print('\n-------------------------------------')
      print('Starting to scrape new datacollection')

      # Get links to relevant observations
      self.GetObservations();

      # If all links are collected create kml and scrape the pages for the data
      print('Starting extraction of data of observations')
      self.CreateWebDriver()
      self.SetLang()
      self.CreateKML()
      self.ScrapePages()
      self.SaveKML()
      self.CloseWebDriver()
      print("Saved as: " + self.Name)




   def StartUpdateSelffindRanking(self):
      print('\n-------------------------------------')
      print('Starting to update the selffind ranking')

      # Get links to relevant observations --> Filter should be here
      self.ImportPoints()
      self.CreateWebDriver()
      self.LogInOld()
      self.SetLang()
      self.GetObservations()
      self.FindSelfFinds()
      self.CloseWebDriver()

   def ImportPoints(self):
      self.Points = {}
      with open("points.json", "r") as config_file:
         self.Points = json.load(config_file)
      

   # Method for collecting all the observations from all pages from the given link
   # This method should be called before ScrapePages()
   def GetObservations(self):
      self.Obs = [];

      # Create variable link such that it is able to go through multiple pages
      BaseLink = self.Link[0:-1]
      Page = 0

      print('Starting to retrieve links from overview pages')

      # Get links from page to observations
      IfEnd = False
      while IfEnd is not True:
         time.sleep(self.Wait)
         Page +=1

         print('Currently in page %d\r'%Page, end="")
         self.Link = BaseLink + str(Page)
         self.GetSoup()

         for link in self.PageSoup.findAll('a', attrs={'href': re.compile("^/observation/")}):
            self.Obs.append(link.get('href'))


         # Check if on last page, if so: end loop.
         LastPage = self.PageSoup.findAll('li', attrs={'last'})[0].find('a').get('href')

         if LastPage == None:
            IfEnd = True
            print('Currently in page ' + str(Page)) 
            print("Found " + str(Page) + " pages of observations having a total of " + str(len(self.Obs)) + " observations.\n")





   # Method to scrape the collected links to observations from GetObservations(). This
   # method can only be called after GetObservations()
   def ScrapePages(self):
      i = 0 
      for iLink in self.Obs:
         # Optional wait to avoid suspicion
         time.sleep(self.Wait)

         i+=1
         ip = i/len(self.Obs)*100
         #if ip < 100:
         #   print('Scraping pages [%d%%]\r'%ip, end="") 
         #else:
         #   print('Scraping pages [100%]')

         self.LinkObs = iLink
         self.CorrectLinkObs()

         CurObservation = Observation(self.LinkObs, self.browser)
         NoGps = CurObservation.GetData();
         # Skip if no gpsdata
         if NoGps is False:
            CurObservation.WriteKMLLine(self.Kml)




   def FindSelfFinds(self):
      PointsTotal = 0
      self.Obs = self.Obs[::-1]
      i = 0 
      for iLink in self.Obs:
         # Optional wait to avoid suspicion
         time.sleep(self.Wait)

         i+=1
         ip = i/len(self.Obs)*100
         #if ip < 100:
         #   print('Looking through pages [%d%%]\r'%ip, end="") 
         #else:
         #   print('Looking through pages [100%]')

         self.LinkObs = iLink
         print(self.LinkObs)
         self.CorrectLinkObs()

         CurObservation = Observation(self.LinkObs, self.browser)
         NoGps = CurObservation.GetData();

         # Check if selffind
         if NoGps is False:
            print("yesGPS")
            IfSelf = CurObservation.CheckSelffind()
            if IfSelf:
               CurObservation.AssignPoints(self.Points)
               PointsTotal +=CurObservation.Point
               CurObservation.WriteOutputLine(self.File)
      self.File.writelines('{:<27}{:>6}'.format("Totaal: ",  PointsTotal))



   # Method to modify a link to an observation such that is is an actual weblink. Not
   # an internal link of waarneming.nl.
   def CorrectLinkObs(self):
      if self.IfOld:
         self.LinkObs = 'https://old.waarneming.nl/waarneming/view/'+self.LinkObs.split("/")[-2]

      else:
         self.LinkObs = 'https://waarneming.nl'+self.LinkObs
         


   # Create .kml file to save observations to.
   def CreateKML(self):
      self.Kml=simplekml.Kml()

   # Saves the created .kml file to self.Name.
   def SaveKML(self):
      self.Kml.save(self.Name, format=True)

   def SetOutputFile(self, File):
      self.File = File








# Class that is used to get the required data of an observation if its link is given. 
# Can be called seperately to test on a single observation.
class Observation(ScrapeBase):


   def __init__(self, Link, browser):
      self.browser = browser;
      self.Link = Link;
      self.SetParam()

   # Method that extracts the data of the webpage of an observation. Can be extended, but
   # it has to be kept in mind that if new data is added, WriteKMLLine() has to be modified
   # to get it in the .kml file.
   def GetData(self):
      self.GetSoup();

      if self.IfOld:
         header = str(self.PageSoup.head.title.text).split("|")[0]  # Find description of observation
         # Find name of species
         self.Name = header.split(" - ")[0]  # Find name of observation

         scripts = self.PageSoup.head.find_all("script")
         #print(len(scripts))
         for i in range(0, len(scripts)):
            if "lon" in str(scripts[i]):
               gps = str(self.PageSoup.head.find_all("script")[i]).split('var')


         #gps = str(self.PageSoup.head.find_all("script")[9]).split('var')
         #print(gps)
         if gps:
            self.Longitude = gps[1].replace('lon =', '').replace(';\n', '')        # Longitude of observation
            self.Latitude = gps[2].replace('lat = ', '').replace(';\n', '')      # Latitude of observation
         else:
            return True

         # Collect details data
         details = self.PageSoup.find_all("p",{"class": "info"})
         if not details:
            self.Description = ''
         else:
            self.Description = [k.text for k in details][0]

         # Find other data of observation in table
         table = self.PageSoup.find_all("table")[2].find_all("td")
         table = [k.text for k in table]

         if 'Datum' in table:
            self.DateTime = table[table.index('Datum') + 1]
         DateTimeList = self.DateTime.replace('-', ' ').split(' ')
         self.Year =  DateTimeList[0]
         self.Month = DateTimeList[1]
         self.Day =   DateTimeList[2]
         self.MonthDay = DateTimeList[2] + "-" + DateTimeList[1]

         if len(DateTimeList) == 4:
            self.Time =  DateTimeList[3]
         else:
            self.Time = '-'

         if 'Gebied' in table:
            self.Location = table[table.index('Gebied') + 1]

         print(self.Name)
         print(self.Description)


         return False
         


      else: 
         self.Name = self.PageSoup.find_all("span",{"class": "species-common-name"})[0].text.strip()
      
         # Datum, Aantal, Levensstadium, Activiteit, Locatie, Waarnemer, Protocol, Telmethode, Methode
         # Only date is implemented
         infotable = self.PageSoup.find_all("table", {"class": "table table-condensed", "id": "observation_details"})
         info = infotable[0].find_all("td")
         self.DateTime = info[0].text.strip()
         DateTimeList = self.DateTime.replace('-', ' ').split(' ')
         self.Year =  DateTimeList[0]
         self.Month = DateTimeList[1]
         self.Day =   DateTimeList[2]
         self.MonthDay = DateTimeList[2] + "-" + DateTimeList[1]
         if len(DateTimeList) == 4:
            self.Time =  DateTimeList[3]
         else:
            self.Time = '-'

         # Get location
         self.Location = info[4].text.strip()



         # Location: skip if obscured
         location = self.PageSoup.find_all("span",{"class": "teramap-coordinates-coords"})
         if location:
            location = location[0].text.strip().split(", ")
         else:
            return True
      
         self.Latitude = location[0]
         self.Longitude = location[1]

         # Find description
         self.Description = self.PageSoup.find("div", {"class": "goog-trans-section"})
         if self.Description:
            if self.Description.find("p"):
               self.Description = self.Description.find("p").contents[0]

         return False







   # Method to write the observation data to the .kml file. If new data is required,
   # it should first be obtained in GetData().
   def WriteKMLLine(self, Kml):
      Kml.newpoint(name = self.Name, coords = [(self.Longitude,self.Latitude)])
      #, description='Date: ' + self.DateTime

   def CheckSelffind(self):
      if self.Description:
         if "Self" in self.Description:
            print("Found selfie")
            return True
         if "self" in self.Description:
            return True


   def WriteOutputLine(self, File):
      File.writelines('{:<27}{:>6}{:>1}{:<10}{:<60}'.format(self.Name, self.Point," " ,self.MonthDay, self.Location))
      File.writelines('\n')

   def AssignPoints(self, Points):
      self.Point = Points[self.Name]



