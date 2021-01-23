# Import classes
from ObsClass import *
from datetime import date

today = date.today()



File = open(r"results.txt","w+")

# Write headers:
File.writelines('{:<20}{:<10}{:<60}{:>20}'.format("Soort", "Datum", "Locatie", "Laatst update: " + str(today)))
File.writelines('\n------------------------------------------------------------------------------------------\n\n\n')



File.writelines('Daan\n\n')
link = "https://waarneming.nl/users/22414/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('Ruben\n\n')
link = "https://waarneming.nl/users/3219/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('Jurri\u00EBn\n\n')
link = "https://waarneming.nl/users/17815/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.writelines('Jacob\n\n')
link = "https://waarneming.nl/users/41541/observations/?after_date=2021-01-01&before_date="+str(today)+"&species_group=1&rarity=2&advanced=on&page=1"
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.close()