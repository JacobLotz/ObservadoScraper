from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import simplekml
import time


# Base class containing methods to get soup and set parameters.
class ScrapeBase:
   def __init__(self, Link):
      self.Link = Link;
      self.SetParam()

   def SetParam(self):
      self.Wait = 0

   
   def GetSoup(self):
      uClient = uReq(self.Link)
      html = uClient.read()
      uClient.close
      self.PageSoup = soup(html, "html.parser")
      print

   def PrintSoup(self):
      print(self.PageSoup)



# Class inheriting from baseclass which creates a collection of observations and uses 
# the class Observation to get its data. Class can be constructed by giving a link 
# and a name.
class ObsCollection(ScrapeBase):

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
      self.CreateKML()
      self.ScrapePages()
      self.SaveKML()
      print("Saved as: " + self.Name)




   def StartUpdateSelffindRanking(self):
      print('\n-------------------------------------')
      print('Starting to update the selffind ranking')

      # Get links to relevant observations --> Filter should be here
      self.GetObservations();
      self.FindSelfFinds()


      

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
            print("Found " + str(Page) + " pages of observations having a total of " + str(len(self.Obs)) + " observations.\n\n")



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
         CurObservation = Observation(self.LinkObs)
         NoGps = CurObservation.GetData();
         # Skip if no gpsdata
         if NoGps is False:
            CurObservation.WriteKMLLine(self.Kml)

   def FindSelfFinds(self):
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

         CurObservation = Observation(self.LinkObs)
         NoGps = CurObservation.GetData();

         # Check if selffind
         if NoGps is False:
            IfSelf = CurObservation.CheckSelffind()
            if IfSelf:
               CurObservation.WriteOutputLine(self.File)


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





# Class that is used to get the required data of an observation if its link is given. 
# Can be called seperately to test on a single observation.
class Observation(ScrapeBase):

   # Method that extracts the data of the webpage of an observation. Can be extended, but
   # it has to be kept in mind that if new data is added, WriteKMLLine() has to be modified
   # to get it in the .kml file.
   def GetData(self):
      self.GetSoup();


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
            return True
         if "self" in self.Description:
            return True


   def WriteOutputLine(self, File):
      File.writelines('{:<20}{:<10}{:<60}'.format(self.Name, self.MonthDay, self.Location))
      File.writelines('\n')
