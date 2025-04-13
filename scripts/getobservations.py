# Import classes
import sys
import os

# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
from classes import *


link = "https://th.observation.org/species/72933/observations/?date_after=2020-10-01&date_before=2024-09-30&page=1"
collection = ObsCollection(link)
collection.SetName("spoon-billed_sandpiper.kml")
collection.StartScrapingProcess()
