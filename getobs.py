# Import classes
from obsclass import *
#from obsclass import Observation
#from obsclass import ObsCollection
#from obsclass import ScrapeBase

link = "https://waarneming.nl/species/290/observations/?after_date=2020-01-01&before_date=2020-12-31&province=10&advanced=on&page=1"
name = "Mibo_2020.kml"
ObsCollection(link, name)

link = "https://waarneming.nl/species/290/observations/?after_date=2019-01-01&before_date=2019-12-31&province=10&advanced=on&page=1"
name = "Mibo_2019.kml"
ObsCollection(link, name)

link = "https://waarneming.nl/species/290/observations/?after_date=2018-01-01&before_date=2018-12-31&province=10&advanced=on&page=1"
name = "Mibo_2018.kml"
ObsCollection(link, name)

link = "https://waarneming.nl/species/290/observations/?after_date=2017-01-01&before_date=2017-12-31&province=10&advanced=on&page=1"
name = "Mibo_2017.kml"
ObsCollection(link, name)



