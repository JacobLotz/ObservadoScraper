#from BaseClass import *
#from MigClass import *
import time
import datetime
import calendar
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

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
year = 2022

month_start = 1;
month_end = 13

bins_start = GetStartDates(month_start, month_end, 2023)
bins_end   = GetEndDates(month_start, month_end, 2023)

# Data storers
dates = [];
squares = [];

link  = "https://old.waarneming.nl/soort/maps/1111?from=" + date.strftime('%Y/%m/%d') + "&to=" + date.strftime('%Y/%m/%d')
migbclass = MigClass(link)
migbclass.CreateWebDriver()


for (date1, date2) in zip(bins_start, bins_end):
	link  = "https://old.waarneming.nl/soort/maps/1111?from=" + date1.strftime('%Y/%m/%d') + "&to=" + date2.strftime('%Y/%m/%d')
	migbclass.UpdateLink(link)
	migbclass.GetSoupMig()

	n = migbclass.GetNSquares()

	# Store data
	squares.append(n)

	print(str(date1) + ", " + str(n) + " squares")




y1 = squares[0::3]
y2 = squares[1::3]
y3 = squares[2::3]

x_axis = [ "Jan", "Feb", "Maa", "Apr", "Mei", "Jun",
           "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]
X_axis = np.arange(len(x_axis))

# Plot
plt.figure(figsize=(8,3))
plt.bar(X_axis - 0.2, y1, 0.2, label = ' 1-10')
plt.bar(X_axis + 0.0, y2, 0.2, label = '11-20')
plt.bar(X_axis + 0.2, y3, 0.2, label = '21-31')
#plt.axvline(x=xm1, linewidth=1.0, color='#d62728')
#plt.axvline(x=xm2, linewidth=1.0, color='#d62728')
plt.xticks(X_axis, x_axis)
#plt.yticks(Y_axis)
#plt.title(title)
plt.legend()
#plt.savefig(file_name)
plt.show()







