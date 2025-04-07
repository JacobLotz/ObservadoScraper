# Import classes
import sys
import os

# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
from classes import *


#link = "https://observation.org/locations/190012/observations/?date_after=2017-04-11&date_before=2024-09-30&species_group=1&page=1"
#collection = ObsCollection(link)
#collection.SetName("siberut.kml")
#collection.StartScrapingProcess()



link = "https://th.observation.org/species/72933/observations/?date_after=2020-10-01&date_before=2024-09-30&page=1"
collection = ObsCollection(link)
collection.SetName("spoon-billed_sandpiper.kml")
collection.StartScrapingProcess()


#link = "https://observation.org/locations/128006/observations/?date_after=2022-01-01&date_before=2024-09-30&species_group=1&rarity=2&advanced=on&page=1"
#collection = ObsCollection(link)
#collection.SetName("spoon-billed_sandpiper.kml")
#collection.StartScrapingProcess()
