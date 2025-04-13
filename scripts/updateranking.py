# Import classes
from datetime import date
import pandas as pd
import sys
import os
 
# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
from classes import *

"""
This script updates the self-found competition by checking the observations of the 
participating members on the markers "self" or "qwery". If the claim should be awarded
with points in the competition it will assign the points and print the details. All
the observations are printed to a file.
"""

start = "2024-01-01"
end = date.today()

filename = parent + "/results.txt"
File = open(filename,"w+")

# Write headers:
File.writelines('{:<27}{:<6}{:<1}{:<10}{:<24}{:<20}'.format("Soort", "Punten", " ","Datum", "Locatie", "Laatste update: " + str(end)))
File.writelines('\n----------------------------------------------------------------------------------------------')


File.writelines('\nDaan\n')
link = "https://waarneming.nl/users/22414/observations/?date_after="+ str(start) +"&date_before="+ str(end) + "&species_group=1&rarity=2&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nRuben\n')
link = "https://waarneming.nl/users/3219/observations/?date_after="+ str(start) +"&date_before="+ str(end) + "&species_group=1&rarity=2&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJurri\u00EBn\n')
link = "https://waarneming.nl/users/17815/observations/?date_after="+ str(start) +"&date_before="+ str(end) + "&species_group=1&rarity=2&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJacob\n')
link = "https://waarneming.nl/users/41541/observations/?date_after="+ str(start) +"&date_before="+ str(end) + "&species_group=1&rarity=2&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.writelines('\n')
File.close()
