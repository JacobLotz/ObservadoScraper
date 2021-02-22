# Import classes
from ObsClass import *
from datetime import date

today = date.today()
link = " https://old.waarneming.nl/user/view/22414?q=&akt=0&g=1&from=2021-01-01&to=" + str(today) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.UnitChecks()