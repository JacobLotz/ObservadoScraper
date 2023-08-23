#from BaseClass import *
#from MigClass import *
import time
import datetime
import calendar
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

def GetMonthEnd(date_in_):
	return calendar.monthrange(date_in_.year, date_in_.month)[1]

def GetStartDates(month_start_, month_end_, year_):
	start_dates = []
	month = month_start_

	while (month != month_end_):
		date = datetime.date(year, month, 1)
		end = GetMonthEnd(date)

		start_dates.append(datetime.date(year, month,  1))
		start_dates.append(datetime.date(year, month, 11))
		start_dates.append(datetime.date(year, month, 21))

		month += 1;
	return start_dates

def GetEndDates(month_start_, month_end_, year_):
	end_dates = []
	month = month_start

	while (month != month_end_):
		date = datetime.date(year, month, 1)
		end = GetMonthEnd(date)

		end_dates.append(datetime.date(year_, month, 11))
		end_dates.append(datetime.date(year_, month, 21))
		end_dates.append(datetime.date(year_, month, end))
		month += 1;
	return end_dates


def divide_chunks(l, n):
	# looping till length l
	for i in range(0, len(l), n): 
		yield l[i:i + n]

# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
from classes import *

# Input
start = datetime.date(2022, 6, 1)
end = datetime.date(2022, 9, 29)

# Define date
date = start
delta = datetime.timedelta(days=10)

# Date bins
year_start = 2020
year_end = 2023
n_years = year_end - year_start + 1

years_range = range(year_start, year_end+1, 1)


month_start = 1;
month_end = 13

bins_start = []
bins_end = []

for year in years_range:
	bins_start_ = GetStartDates(month_start, month_end, year)
	bins_end_   = GetEndDates(month_start, month_end, year)

	bins_start.extend(bins_start_)
	bins_end.extend(bins_end_)

# Data storers
dates = [];
squares = [];

link  = "https://old.waarneming.nl/soort/maps/361?from=" + date.strftime('%Y/%m/%d') + "&to=" + date.strftime('%Y/%m/%d')
migbclass = MigClass(link)
migbclass.CreateWebDriver()


for (date1, date2) in zip(bins_start, bins_end):
	link  = "https://old.waarneming.nl/soort/maps/361?from=" + date1.strftime('%Y/%m/%d') + "&to=" + date2.strftime('%Y/%m/%d')
	migbclass.UpdateLink(link)
	migbclass.GetSoupMig()

	n = migbclass.GetNSquares()

	# Store data
	squares.append(n)

	print(str(date1) + ", " + str(n) + " squares")


# Plot
x_axis = [ "Jan", " ", " ", "Feb", " ", " ", "Maa", " ", " ", "Apr", " ", " ", "Mei", " ", " ", "Jun", " ", " ",
           "Jul", " ", " ", "Aug", " ", " ", "Sep", " ", " ", "Okt", " ", " ", "Nov", " ", " ", "Dec", " ", " ",]
X_axis = np.arange(len(x_axis))

y = squares
yy = list(divide_chunks(y, len(x_axis)))

#print(*map(mean, zip(*yy)))

#yy_mean = map(mean, zip(*yy))
yy_mean = np.mean(np.array(yy), axis=0).tolist()
print(yy_mean)

plt.figure(figsize=(8,3))
for (yyy, year) in zip(yy,years_range):
	plt.plot(X_axis, yyy, label = str(year),  alpha=0.5, linestyle='dashed')
plt.plot(X_axis, yy_mean, color="black", label = "average")
plt.xticks(X_axis, x_axis)
#plt.title(title)
plt.legend()
#plt.savefig(file_name)
plt.show()




