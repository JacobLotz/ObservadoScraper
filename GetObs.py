# Import classes
from ObsClass import *

link = "https://waarneming.nl/species/290/observations/?after_date=2020-01-01&before_date=2020-12-31&province=10&advanced=on&page=1"
name = "Mibo_2020.kml"
collection = ObsCollection(link, name)
collection.StartScrapingProcess()


link = "https://waarneming.nl/species/290/observations/?after_date=2019-01-01&before_date=2019-12-31&province=10&advanced=on&page=1"
name = "Mibo_2019.kml"
collection = ObsCollection(link, name)
collection.StartScrapingProcess()

link = "https://waarneming.nl/species/290/observations/?after_date=2018-01-01&before_date=2018-12-31&province=10&advanced=on&page=1"
name = "Mibo_2018.kml"
collection = ObsCollection(link, name)
collection.StartScrapingProcess()

link = "https://waarneming.nl/species/290/observations/?after_date=2017-01-01&before_date=2017-12-31&province=10&advanced=on&page=1"
name = "Mibo_2017.kml"
collection = ObsCollection(link, name)
collection.StartScrapingProcess()



