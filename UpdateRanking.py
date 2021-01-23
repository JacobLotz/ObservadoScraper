
# Import classes
from ObsClass import *

link = "https://waarneming.nl/species/290/observations/?after_date=2020-01-01&before_date=2020-12-31&province=10&advanced=on&page=1"
name = "Mibo_2020.kml"
collection = ObsCollection(link, name)
collection.StartScrapingProcess()