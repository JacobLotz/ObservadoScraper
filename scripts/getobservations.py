# Import classes
from ObsClass import *

link = "https://waarneming.nl/locations/22901/observations/?species=337&after_date=1992-01-17&before_date=2021-03-21&page=1"
collection = ObsCollection(link)
#collection.SetName("kortsnavel.kml")
collection.StartScrapingProcess()


#link = "https://waarneming.nl/species/290/observations/?after_date=2020-01-01&before_date=2020-12-31&province=&advanced=on&page=1"
#collection = ObsCollection(link)
#collection.SetName("Mibo_2020.kml")
#collection.StartScrapingProcess()


#link = "https://waarneming.nl/species/290/observations/?after_date=2019-01-01&before_date=2019-12-31&province=&advanced=on&page=1"
#collection = ObsCollection(link)
#collection.SetName("Mibo_2019.kml")
#collection.StartScrapingProcess()

#link = "https://waarneming.nl/species/290/observations/?after_date=2018-01-01&before_date=2018-12-31&province=&advanced=on&page=1"
#collection = ObsCollection(link)
#collection.SetName("Mibo_2018.kml")
#collection.StartScrapingProcess()

#link = "https://waarneming.nl/species/290/observations/?after_date=2017-01-01&before_date=2017-12-31&province=&advanced=on&page=1"
#collection = ObsCollection(link)
#collection.SetName("Mibo_2017.kml")
#collection.StartScrapingProcess()



