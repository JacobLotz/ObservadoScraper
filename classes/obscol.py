import re
import simplekml
import time
import json
from selenium.webdriver.common.keys import Keys
import os

import time

from .obs import Observation
from .base import ScrapeBase

# import password from external file
from passwords.passwords import username_in, password_in

# Class inheriting from baseclass which creates a collection of observations and uses 
# the class Observation to get its data. Class can be constructed by giving a link 
# and a name.
class ObsCollection(ScrapeBase):

   def __init__(self, Link):
      super().__init__(Link)
      self.Name = "out.kml"
    # body of the constructor


   def SetName(self, kmlname):
      self.Name = kmlname


   # Log into old website
   def LogIn(self):
      url = 'https://waarneming.nl/accounts/login/?next=/'
      self.browser.get(url)
      user_name = self.browser.find_element("name","login")
      user_name.send_keys(username_in)
      password = self.browser.find_element("name",'password')
      password.send_keys(password_in)
      password.send_keys(Keys.RETURN)


   # Set language for new website
   def SetLang(self):
      url = "https://waarneming.nl/generic/select-language-modal/"
      self.browser.get(url)
      time.sleep(3)
      button = self.browser.find_element("xpath", "//button[@value='"+self.Lang+"']")
      button.click()


   # Method for performing the whole scraping process after initialization for new website
   def StartScrapingProcess(self):
      print('\n-------------------------------------')
      print('Starting to scrape new datacollection')

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

      # Get links to relevant observations --> Filter should be here
      self.ImportPoints()
      self.CreateWebDriver()
      #self.LogIn()
      self.SetLang()
      self.GetObservationsSelf()
      self.FindSelfFinds()
      self.CloseWebDriver()


   # Method which imports the point for the selffind rankin
   def ImportPoints(self):
      self.Points = {}

      parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
      filename = os.path.join(parent_dir, 'results.txt')
      os.path.join(parent_dir, 'data/points.json')
      with open(os.path.join(parent_dir, 'data/points.json'), "r") as config_file:
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
         try:
            LastPage = self.PageSoup.findAll('li', attrs={'last'})[0].find('a').get('href')
         except: # Exception for one page
            LastPage = None

         if LastPage == None:
            IfEnd = True
            print('Currently in page ' + str(Page)) 
            print("Found " + str(Page) + " pages of observations having a total of " + str(len(self.Obs)) + " observations.\n")


   # Method for collecting all the observations from all pages from the given link for new website
   # This method should be called before ScrapePages() 
   def GetObservationsSelf(self):
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


         links=[]
         for link in self.PageSoup.findAll('a', attrs={'href': re.compile("^/observation/")}):
            links.append(link.get('href'))

         species = self.PageSoup.findAll("span",{"class": ["species-common-name"]})
         potentialselfobs = []

         i = 0
         for sp in species:
            testspecies = sp.get_text()#.split(" - ")[0]

            if testspecies in self.Points:
               potentialselfobs.append(i)
            i+=1

         # Get potential links
         for i in potentialselfobs:
            self.Obs.append(links[i])

         # Check if on last page, if so: end loop.
         try:
            LastPage = self.PageSoup.findAll('li', attrs={'last'})[0].find('a').get('href')
         except: # Exception for one page
            LastPage = None

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
         if ip < 100:
            print('Scraping pages [%d%%]\r'%ip, end="") 
         else:
            print('Scraping pages [100%]')

         self.LinkObs = iLink
         self.CorrectLinkObs()

         CurObservation = Observation(self.LinkObs, self.browser)
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
      self.LinkObs = 'https://waarneming.nl'+self.LinkObs
         

   # Create .kml file to save observations to.
   def CreateKML(self):
      self.Kml=simplekml.Kml()

   # Saves the created .kml file to self.Name.
   def SaveKML(self):
      self.Kml.save(self.Name, format=True)

   def SetOutputFile(self, File):
      self.File = File
      
