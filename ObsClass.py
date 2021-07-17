from bs4 import BeautifulSoup as soup
import re
import simplekml
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from BaseClass import *
from Observation import *


# Class inheriting from baseclass which creates a collection of observations and uses 
# the class Observation to get its data. Class can be constructed by giving a link 
# and a name.
class ObsCollection(ScrapeBase):
   def CreateWebDriver(self):
      self.browser = webdriver.Chrome(executable_path = self.pathdriver, chrome_options = self.chrome_options)

   def CloseWebDriver(self):
      self.browser.quit()

   # Log into old website
   def LogIn(self):
      url = 'https://waarneming.nl/accounts/login/?next=/'
      self.browser.get(url)
      user_name = self.browser.find_element_by_name("login")
      user_name.send_keys("lotzzzz")
      password = self.browser.find_element_by_name('password')
      password.send_keys("jacoblotz")
      password.send_keys(Keys.RETURN)

   # Log into new website
   def LogInOld(self):
      url = 'https://old.waarneming.nl/user/login'
      self.browser.get(url)
      user_name = self.browser.find_element_by_name("user")
      user_name.send_keys("lotzzzz")
      password = self.browser.find_element_by_name('password')
      password.send_keys("jacoblotz")
      password.send_keys(Keys.RETURN)

   # Set language for new website
   def SetLang(self):
      url = "https://waarneming.nl/generic/select-language-modal/"
      self.browser.get(url)
      button = self.browser.find_elements_by_name("language")
      button = button[35]
      button.click()
      
      

   # Method for performing the whole scraping process after initialization for new website
   def StartScrapingProcess(self):
      print('\n-------------------------------------')
      print('Starting to scrape new datacollection')

      # Check if old website or new website, this scraper can handle both
      if "old.waarneming" in self.Link:
         self.IfOld = True
      else:
         self.IfOld = False

      if self.IfOld:
         # Get links to relevant observations
         self.CreateWebDriver()
         self.GetObservationsOld();
         
         # If all links are collected create kml and scrape the pages for the data
         print('Starting extraction of data of observations')
         
         self.CreateKML()
         self.ScrapePages()
         self.SaveKML()
         self.CloseWebDriver()
         print("Saved as: " + self.Name)

      else:   
         # Get links to relevant observations
         self.CreateWebDriver()
         self.SetLang()
         self.GetObservations();

         # If all links are collected create kml and scrape the pages for the data
         print('Starting extraction of data of observations')

         self.CreateKML()
         self.ScrapePages()
         self.SaveKML()
         self.CloseWebDriver()
         print("Saved as: " + self.Name)



   # Method for performing the whole scraping process after initialization for old website
   def StartUpdateSelffindRanking(self):
      print('\n-------------------------------------')
      print('Starting to update the selffind ranking')

      # Check if old website or new website, this scraper can handle both
      if "old.waarneming" in str(self.Link):
         self.IfOld = True
      else:
         self.IfOld = False

      # Get links to relevant observations --> Filter should be here
      if self.IfOld:
         self.ImportPoints()
         self.CreateWebDriver()
         self.LogInOld()
         self.GetObservationsSelfOld()
         self.FindSelfFinds()
         self.CloseWebDriver()
      else:
         self.ImportPoints()
         self.CreateWebDriver()
         self.LogIn()
         self.SetLang()
         self.GetObservations()
         self.FindSelfFinds()
         self.CloseWebDriver()

   # Method which imports the point for the selffind rankin
   def ImportPoints(self):
      self.Points = {}
      with open("points.json", "r") as config_file:
         self.Points = json.load(config_file)
      

   # Method for collecting all the observations from all pages from the given link for new website
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




   # Method for collecting all the observations from all pages from the given link for OLD website
   # This method should be called before ScrapePages() 
   def GetObservationsOld(self):
      self.Obs = [];

      # Create variable link such that it is able to go through multiple pages
      BaseLink = self.Link[0:-1]
      Page = 0

      print('Starting to retrieve links from overview pages')

      # Find last page
      self.GetSoup()
      lastpage = int(str(self.PageSoup.find("td", colspan = True)).split(" | ")[1].split(" ")[0])

      # Get links from page to observations
      IfEnd = False
      while IfEnd is not True:
         time.sleep(self.Wait)
         Page +=1

         print('Currently in page %d\r'%Page, end="")
         self.Link = BaseLink + str(Page)
         self.GetSoup()

         for link in self.PageSoup.findAll('a', attrs={'href': re.compile("^/waarneming/view/")}):
            self.Obs.append(link.get('href'))

         if Page == lastpage:
            IfEnd = True
            print('Currently in page ' + str(Page))

            # Remove duplicates
            TempObs = []
            for i in self.Obs:
               if i not in TempObs:
                  TempObs.append(i)
            self.Obs = TempObs
            print("Found " + str(Page) + " pages of observations having a total of " + str(len(self.Obs)) + " observations.\n")
   

   # Method for collecting all the observations from all pages from the given link for OLD website
   # This method should be called before ScrapePages() ONLY SAVING POTENTIAL SELFFINDS
   

   def GetObservationsSelfOld(self):
      self.Obs = [];

      # Create variable link such that it is able to go through multiple pages
      BaseLink = self.Link[0:-1]
      Page = 0

      print('Starting to retrieve links from overview pages')

      # Find last page
      self.GetSoup()
      lastpage = int(str(self.PageSoup.find("td", colspan = True)).split(" | ")[1].split(" ")[0])


      # Get links from page to observations
      IfEnd = False
      
      while IfEnd is not True:
         Page +=1
         time.sleep(self.Wait)
         print('Currently in page %d\r'%Page, end="")
         self.Link = BaseLink + str(Page)
         self.GetSoup()

         links = self.PageSoup.findAll('a', attrs={'href': re.compile("^/waarneming/view/")})
         species = self.PageSoup.findAll("span",{"class": ["z2", "z3", "z4"]})
         testlinks = []
         potentialselfobs = []
         
         i = 0
         for sp in species:
            testspecies = sp.get_text().split(" - ")[0]
            if testspecies in self.Points:
               potentialselfobs.append(i)
            i+=1

         for link in links:
            testlinks.append(link.get('href'))

         # Remove duplicates
         TempObs = []
         for i in range(0,len(testlinks),2):
            TempObs.append(testlinks[i])
         testlinks = TempObs

        
         # Get potential links
         for i in potentialselfobs:
            self.Obs.append(testlinks[i])

         if Page == lastpage:
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
         if ip < 100:
            print('Scraping pages [%d%%]\r'%ip, end="") 
         else:
            print('Scraping pages [100%]')

         self.LinkObs = iLink
         self.CorrectLinkObs()

         CurObservation = Observation(self.LinkObs, self.browser)
         if self.IfOld:
            NoGps = CurObservation.GetDataOld();
         else:
            NoGps = CurObservation.GetData();
         
         
         # Skip if no gpsdata
         if NoGps is False:
            CurObservation.WriteKMLLine(self.Kml)



   # Method which finds all selffind observations and writes to file after initalisation
   def FindSelfFinds(self):
      PointsTotal = 0
      self.Obs = self.Obs[::-1]
      i = 0 
      for iLink in self.Obs:
         # Optional wait to avoid suspicion
         time.sleep(self.Wait)

         i+=1
         ip = i/len(self.Obs)*100
         if ip < 100:
            print('Looking through pages [%d%%]\r'%ip, end="") 
         else:
            print('Looking through pages [100%]')

         self.LinkObs = iLink
         self.CorrectLinkObs()

         CurObservation = Observation(self.LinkObs, self.browser)
         if self.IfOld:
            NoGps = CurObservation.GetDataOld();
         else:
            NoGps = CurObservation.GetData();

         # Check if selffind
         if NoGps is False:
            IfSelf = CurObservation.CheckSelffind()
            if ((IfSelf) and (CurObservation.Name in self.Points)):
               CurObservation.AssignPoints(self.Points)
               PointsTotal +=CurObservation.Point
               CurObservation.WriteOutputLine(self.File)
      self.File.writelines('\n')
      self.File.writelines('{:<27}{:>6}'.format("Totaal: ",  PointsTotal))




   # Method to modify a link to an observation such that is is an actual weblink. Not
   # an internal link of waarneming.nl.
   def CorrectLinkObs(self):
      if self.IfOld:
         self.LinkObs = 'https://old.waarneming.nl'+self.LinkObs

      else:
         self.LinkObs = 'https://waarneming.nl'+self.LinkObs
         


   # Create .kml file to save observations to.
   def CreateKML(self):
      self.Kml=simplekml.Kml()

   # Saves the created .kml file to self.Name.
   def SaveKML(self):
      self.Kml.save("out.kml", format=True)

   def SetOutputFile(self, File):
      self.File = File

   def UnitCheckObs(self):
      if "Raaf" not in self.Observation.Name:
         print("Error in name")
      #print(self.Observation.Name)

      if "52.03" not in str(self.Observation.Latitude):
         print("Error in Latitude")
         print(self.Observation.Latitude)

      if "5.37" not in str(self.Observation.Longitude):
         print("Error in Longitude")
         print(self.Observation.Longitude)





   def UnitChecks(self):
      # Old Website
      self.CreateWebDriver()
      self.LogInOld()
      link = "https://old.waarneming.nl/waarneming/view/207490728" 
      self.Observation = Observation(link, self.browser)
      NoGps = self.Observation.GetDataOld();
      self.UnitCheckObs()
      self.CloseWebDriver()

      # New website
      self.CreateWebDriver()
      self.LogIn()
      self.SetLang()
      link = "https://waarneming.nl/observation/207490728/" 
      self.Observation = Observation(link, self.browser)
      NoGps = self.Observation.GetData();
      self.UnitCheckObs()
      self.CloseWebDriver()

      # GetObservations old website
      self.CreateWebDriver()
      self.LogInOld()
      self.Link = "https://old.waarneming.nl/user/view/41541?q=&akt=0&g=0&from=2021-01-01&to=2021-01-06&prov=0&z=0&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1"
      self.GetObservationsOld()
      if len(self.Obs) != 56:
         print("Error in GetObservationsOld")
         print(len(self.Obs))
      self.CloseWebDriver()

      # GetObservations new website
      self.CreateWebDriver()
      self.LogIn()
      self.Link = "https://waarneming.nl/users/41541/observations/?after_date=2021-01-01&before_date=2021-01-06&species_group=&rarity=&search=&species=&sex=&province=&validation_status=&life_stage=&activity=&method3/users/41541/observations/?after_date=2021-01-01&before_date=2021-01-06&page=1"
      self.GetObservations()
      if len(self.Obs) != 56:
         print("Error in GetObservations")
         print(len(self.Obs))
      self.CloseWebDriver()
      







