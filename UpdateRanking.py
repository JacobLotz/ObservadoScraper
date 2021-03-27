# Import classes
from ObsClass import *
from datetime import date
import pandas as pd

"""
df = pd.DataFrame(columns = ['Observer', 'Name', 'Point', 'Location', 'MonthDay'])

df = df.append({'Observer':'Daan', 'Name': 'Roodhalsgans','Point': 4.0, 'Location' : 'Amsterdam','MonthDay':'01-01-21'}, ignore_index=True)

df = df.append({'Observer':'Jurrien', 'Name': 'Kortsnavelboomkruiper','Point': 4.0, 'Location' : 'Veluwe','MonthDay':'01-03-21'}, ignore_index=True)

df = df.append({'Observer':'Jurrien', 'Name': 'Zeearend','Point': 4.0, 'Location' : 'Rectum','MonthDay':'01-05-21'}, ignore_index=True)

df = df.append({'Observer':'Ruben', 'Name': 'Rode wouw','Point': 0.5, 'Location' : 'Rectum','MonthDay':'01-05-21'}, ignore_index=True)

df = df.append({'Observer':'Jacob', 'Name': 'Europese kanarie','Point': 1.0, 'Location' : 'Rectum','MonthDay':'01-05-21'}, ignore_index=True)



# Get sum of observer
print(df.loc[df['Observer'] == "Jurrien"]['Point'].sum())


print("\n\n\n")
# Get observations of observer
print(df.loc[df['Observer'] == "Jurrien"])


print("\n\n\n")
# Get specific obervation of observer
print(df.loc[df['Observer'] == "Jurrien"].iloc[0])

# Get column info
print(df.loc[df['Observer'] == "Jurrien"].iloc[0]['Name'])

print("\n\n\n")
# Get number of rows
print(df.shape[0])

# Print dataframe
print("\n\n\n")
print(df)

# Print unique observers
print(df['Observer'].unique())

# Print all data of specific observer
print("\n\n\n")
df2 = df.loc[df['Observer'] == "Jurrien"]
i = 0
while i < (df2.shape[0]):
   print('{:<27}{:>6}{:>1}{:<10}{:<60}'.format(
      df2.iloc[i]['Name'], 
      df2.iloc[i]['Point'],
      " " , 
      df2.iloc[i]['MonthDay'],
      df2.iloc[i]['Location']
      ))
   i+=1


# Print all data of all observers // Use File.writelines() to print to file
print("\n\n\n")

for d in df['Observer'].unique():
   print(d)
   df2 = df.loc[df['Observer'] == d]
   i = 0
   while i < (df2.shape[0]):
      print('{:<27}{:>6}{:>1}{:<10}{:<60}'.format(
         df2.iloc[i]['Name'], 
         df2.iloc[i]['Point'],
         " " , 
         df2.iloc[i]['MonthDay'],
         df2.iloc[i]['Location']
         ))
      i+=1
   print("")


# Create ranking
print("\n\n\n")


maxpoints1 = 0
rank = 0
check  = 0
df2 = df.copy()
print('Ranking')
while rank != 4:
   maxpoints1 = 0
   maxpoints2 = 0
   for d in df['Observer'].unique():
      maxpoints2 = df2.loc[df['Observer'] == d]['Point'].sum()
      if maxpoints2 > maxpoints1:
         maxpoints1 = maxpoints2
         maxobserver = d
   rank += 1


   df2.drop(df[df['Observer'] == maxobserver].index, inplace = True)  
   print('{:<4}{:<15}{:>6}'.format(rank, maxobserver, maxpoints1))


"""







today = date.today()
File = open(r"results.txt","w+")

# Write headers:
File.writelines('{:<27}{:<6}{:<1}{:<10}{:<24}{:<20}'.format("Soort", "Punten", " ","Datum", "Locatie", "Laatste update: " + str(today)))
File.writelines('\n----------------------------------------------------------------------------------------------')




File.writelines('\nDaan\n')
link = " https://old.waarneming.nl/user/view/22414?q=&akt=0&g=1&from=2021-01-01&to=" + str(today) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nRuben\n')
link = " https://old.waarneming.nl/user/view/3219?q=&akt=0&g=1&from=2021-01-01&to=" + str(today) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJurri\u00EBn\n')
link = " https://old.waarneming.nl/user/view/17815?q=&akt=0&g=1&from=2021-01-01&to=" + str(today) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()

File.writelines('\n\n----------------------------------------------------------------------------------------------')
File.writelines('\nJacob\n')
link = " https://old.waarneming.nl/user/view/41541?q=&akt=0&g=1&from=2021-01-01&to=" + str(today) + "&prov=0&z=2&sp=0&gb=0&method=0&cdna=0&f=0&m=K&zeker=O&month=0&rows=20&only_hidden=0&zoektext=0&tag=0&plum=0&page=1" 
collection = ObsCollection(link)
collection.SetOutputFile(File)
collection.StartUpdateSelffindRanking()


File.writelines('\n')
File.close()