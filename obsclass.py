from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import simplekml
import time

class ScrapeBase:
   def __init__(self, Link):
      self.Link = Link;
      self.Wait = 0
      self.SetParam()

   def SetParam(self):
      self.Wait = 0

   
   def GetSoup(self):
      uClient = uReq(self.Link)
      html = uClient.read()
      uClient.close
      self.pagesoup = soup(html, "html.parser")
      print

   def PrintSoup(self):
      print(self.pagesoup)



class ObsCollection(ScrapeBase):

   def __init__(self, Link, Name):
      self.Link = Link;
      self.Name = Name;
      self.SetParam();
      print('\n-------------------------------------')
      print('Starting to scrape new datacollection')
      self.GetObservations();

   def GetObservations(self):
      self.Obs = [];

      # Create variable in link
      BaseLink = self.Link[0:-1]
      page = 0

      print('Starting to retrieve links from overview pages')

      # Get links from page to observations
      ifend = False
      while ifend is not True:
         time.sleep(self.Wait)
         page +=1

         print('Currently in page %d\r'%page, end="")
         #print('Currently in page ' + str(page), end="") 


         self.Link = BaseLink + str(page)
         self.GetSoup()
         for link in self.pagesoup.findAll('a', attrs={'href': re.compile("^/observation/")}):
            self.Obs.append(link.get('href'))
         
         lastpage = self.pagesoup.findAll('li', attrs={'last'})[0].find('a').get('href')
         if lastpage == None:
            ifend = True
            print('Currently in page ' + str(page)) 
            print("Found " + str(page) + " pages of observations having a total of " + str(len(self.Obs)) + " observations.")


      # If all links are collected create kml and scrape the pages for the data
      print('Starting extraction of data of observations')
      self.CreateKML()
      self.ScrapePages()
      self.SaveKML()
      print("Saved as: " + self.Name)

      
   def ScrapePages(self):
      i = 0 
      for link in self.Obs:
         # Wait to avoid suspicion
         time.sleep(self.Wait)

         i+=1
         ip = i/len(self.Obs)*100
         if ip < 100:
            print('Scraping pages [%d%%]\r'%ip, end="") 
         else:
            print('Scraping pages [100%]')

         self.LinkObs = link
         self.CorrectLinkObs()
         observation = Observation(self.LinkObs)
         nogps = observation.GetData();
         if nogps is False:
            observation.WriteKMLLine(self.kml)

   def CorrectLinkObs(self):
      self.LinkObs = 'https://waarneming.nl'+self.LinkObs

   def CreateKML(self):
      self.kml=simplekml.Kml()

   def SaveKML(self):
      self.kml.save(self.Name, format=True)






class Observation(ScrapeBase):  

   def GetData(self):
      self.GetSoup();


      self.Name = self.pagesoup.find_all("span",{"class": "species-common-name"})[0].text.strip()
      
      # Datum, Aantal, Levensstadium, Activiteit, Locatie, Waarnemer, Protocol, Telmethode, Methode
      # Only date is implemented
      infotable = self.pagesoup.find_all("table", {"class": "table table-condensed", "id": "observation_details"})
      info = infotable[0].find_all("td")
      self.DateTime = info[0].text.strip()
      DateTimeList = self.DateTime.replace('-', ' ').split(' ')
      self.Year =  DateTimeList[0]
      self.Month = DateTimeList[1]
      self.Day =   DateTimeList[2]
      if len(DateTimeList) == 4:
         self.Time =  DateTimeList[3]
      else:
         self.Time = '-'

      # Location: skip if obscured
      location = self.pagesoup.find_all("span",{"class": "teramap-coordinates-coords"})
      if location:
         location = location[0].text.strip().split(", ")
      else:
         return True
      
      self.Latitude = location[0]
      self.Longitude = location[1]

      return False



   def WriteKMLLine(self, kml):
      kml.newpoint(name = self.Name, coords = [(self.Longitude,self.Latitude)])
#, description='Date: ' + self.DateTime

