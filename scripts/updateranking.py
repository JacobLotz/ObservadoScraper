# Import classes
from ObsClass import *
from datetime import date
import pandas as pd

"""
This script updates the self-found competition by checking the observations of the 
participating members on the markers "self" or "qwery". If the claim should be awarded
with points in the competition it will assign the points and print the details. All
the observations are printed to a file.
"""

start = "2022-01-01"
#end = "2021-05-09"
end = date.today()
File = open(r"results.txt","w+")

# Write headers:
File.writelines('{:<27}{:<6}{:<1}{:<10}{:<24}{:<20}'.format("Soort", "Punten", " ","Datum", "Locatie", "Laatste update: " + str(end)))
File.writelines('\n----------------------------------------------------------------------------------------------')




File.writelines('\nDaan\n')
link = " https://old.waarneming.nl/user/view/22414?q=&akt=0&g=1&from=" + str(start) + "&to=" + str(end) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nRuben\n')
link = " https://old.waarneming.nl/user/view/3219?q=&akt=0&g=1&from=" + str(start) + "&to=" + str(end) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJurri\u00EBn\n')
link = " https://old.waarneming.nl/user/view/17815?q=&akt=0&g=1&from=" + str(start) + "&to=" + str(end) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJacob\n')
link = " https://old.waarneming.nl/user/view/41541?q=&akt=0&g=1&from=" + str(start) + "&to=" + str(end) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.writelines('\n')
File.close()
