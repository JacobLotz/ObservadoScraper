from BaseClass import *
import time

link = "https://old.waarneming.nl/soort/maps/227?from=2020-07-17&to=2021-07-17"


base = ScrapeBase(link)
base.CreateWebDriver()
base.GetSoupMig()

test = str(base.PageSoup.find("svg",{"class": "leaflet-zoom-animated"})).split("<g>")

print(test)
print(len(test))

#.find_all("g")


#base.PrintSoup();




