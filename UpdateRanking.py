# Import classes
from ObsClass import *
from datetime import date

today = date.today()
File = open(r"results.txt","w+")

# Write headers:
File.writelines('{:<27}{:<6}{:<1}{:<10}{:<24}{:<20}'.format("Soort", "Punten", " ","Datum", "Locatie", "Laatste update: " + str(today)))
File.writelines('\n----------------------------------------------------------------------------------------------')




File.writelines('\n\nDaan\n')
link = "https://waarneming.nl/users/22414/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\nRuben\n')
link = "https://waarneming.nl/users/3219/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\nJurri\u00EBn\n')
link = "https://waarneming.nl/users/17815/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.writelines('\n\nJacob\n')
link = "https://waarneming.nl/users/41541/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()



File.close()