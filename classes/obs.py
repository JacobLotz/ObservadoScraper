from classes import *

# Class that is used to get the required data of an observation if its link is given. 
# Can be called seperately to test on a single observation.
class Observation(ScrapeBase):

   def __init__(self, Link, browser):
      self.browser = browser;
      self.Link = Link;
      self.SetParam()

   # Method that extracts the data of the webpage of an observation. Can be extended, but
   # it has to be kept in mind that if new data is added, WriteKMLLine() has to be modified
   # to get it in the .kml file. FOR NEW WEBSITE
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
         self.Description = self.Description.get_text()

      return False


   # Method to write the observation data to the .kml file. If new data is required,
   # it should first be obtained in GetData().
   def WriteKMLLine(self, Kml):
      Kml.newpoint(name = self.Name, coords = [(self.Longitude,self.Latitude)], description='Date: ' + self.DateTime)


   # Method which checks if the observation is a selffind.
   def CheckSelffind(self):
      if self.Description:
         if "Self" in self.Description:
            return True
         if "self" in self.Description:
            return True
         if "qwerty" in self.Description:
            return True
         if "Qwerty" in self.Description:
            return True


   def WriteOutputLine(self, File):
      File.writelines('{:<27}{:>6}{:>1}{:<10}{:<60}'.format(self.Name, self.Point," " ,self.MonthDay, self.Location))
      File.writelines('\n')


   def AssignPoints(self, Points):
      self.Point = Points[self.Name]
