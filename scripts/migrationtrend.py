#from BaseClass import *
#from MigClass import *
import time
import datetime
import sys
import os
 



# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
from classes import *


# Input
start = datetime.date(2022, 7, 15)
end = datetime.date(2022, 8, 15)



# Define date
date = start
delta = datetime.timedelta(days=1)



dates = [];
squares =[];

while (date != end):

	link  = "https://old.waarneming.nl/soort/maps/1111?from=" + date.strftime('%Y/%m/%d') + "&to=" + date.strftime('%Y/%m/%d')
	migbclass = MigClass(link)
	migbclass.CreateWebDriver()
	migbclass.GetSoupMig()
	n = migbclass.GetNSquares()

	print(date)
	print(n)
	print('\n')

	dates.append(date.strftime('%Y/%m/%d'))
	squares.append(n)

	date = date + delta


print(dates)
print('\n')
print(squares)








