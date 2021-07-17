from BaseClass import *
import time

link = "https://old.waarneming.nl/soort/maps/227?from=2020-07-17&to=2021-07-17"


base = ScrapeBase(link)
base.CreateWebDriver()
base.GetSoup()

print(base.PageSoup.find_all("svg",{"class": "leaflet-clickable"}))

#.find_all("g")


#base.PrintSoup();




