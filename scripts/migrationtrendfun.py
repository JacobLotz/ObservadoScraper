import datetime
import calendar
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

from classes import *


def GetMonthEnd(date_in_):
	return calendar.monthrange(date_in_.year, date_in_.month)[1]


def GetStartDates(month_start_, month_end_, year_):
	start_dates = []
	month = month_start_

	while (month != month_end_+1):
		date = datetime.date(year_, month, 1)
		end = GetMonthEnd(date)

		start_dates.append(datetime.date(year_, month,  1))
		start_dates.append(datetime.date(year_, month, 11))
		start_dates.append(datetime.date(year_, month, 21))

		month += 1;
	return start_dates


def GetEndDates(month_start_, month_end_, year_):
	end_dates = []
	month = month_start_

	while (month != month_end_+1):
		date = datetime.date(year_, month, 1)
		end = GetMonthEnd(date)

		end_dates.append(datetime.date(year_, month, 11))
		end_dates.append(datetime.date(year_, month, 21))
		end_dates.append(datetime.date(year_, month, end))
		month += 1;
	return end_dates


def DivideChunks(l, n):
	# looping till length l
	for i in range(0, len(l), n): 
		yield l[i:i + n]


def GetSpeciesPlot(year_start, year_end, month_start, month_end, speciesid, name):
	print("Working on: " + name)

	# Date bins
	n_years = year_end - year_start + 1
	years_range = range(year_start, year_end+1, 1)

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

	# Data collection
	link  = "https://old.waarneming.nl/"
	migbclass = MigClass(link)
	migbclass.CreateWebDriver()

	for (date1, date2) in zip(bins_start, bins_end):
		link = "https://waarneming.nl/species/"+str(speciesid)+"/maps/?start_date=" + date1.strftime('%Y-%m-%d') + "&end_date=" + date2.strftime('%Y-%m-%d')+"&map_type=grid1k"

		migbclass.UpdateLink(link)
		migbclass.GetSoupMig()

		n = migbclass.GetNSquares()

		# Store data
		squares.append(n)

		print(str(date1) + ", " + str(n) + " squares")

	# Labels
	x_axis = [ "Jan", " ", " ", "Feb", " ", " ", "Maa", " ", " ", "Apr", " ", " ", "Mei", " ", " ", "Jun", " ", " ",
	           "Jul", " ", " ", "Aug", " ", " ", "Sep", " ", " ", "Okt", " ", " ", "Nov", " ", " ", "Dec", " ", " ",]

	X_axis = np.arange(len(x_axis))

	x_axis = x_axis[(month_start - 1)*3:(month_end*3)]
	X_axis = np.arange(len(x_axis))

	y = squares
	yy = list(DivideChunks(y, len(x_axis)))

	# Compute mean, but do not include last year in average
	if len(yy)>0:
		yy_premean = yy[0:-1]

	yy_mean = np.mean(np.array(yy_premean), axis=0).tolist()

	# Axis locators
	majorLocator   = MultipleLocator(3)
	minorLocator   = MultipleLocator(1)

	# Plot
	plt.figure(figsize=(8,3))
	for (yyy, year) in zip(yy,years_range):
		plt.plot(X_axis + 0.5, yyy, label = str(year),  alpha=0.5, linestyle='dashed')
	plt.plot(X_axis + 0.5, yy_mean, color="black", label = "gem.")

	plt.gca().set_ylim(bottom=0)
	plt.gca().set_xlim(left=0, right=len(x_axis))

	plt.xticks(X_axis, x_axis)
	plt.gca().xaxis.set_major_locator(majorLocator)
	plt.gca().xaxis.set_minor_locator(minorLocator)

	plt.title(name)
	plt.legend()
	plt.savefig(str(speciesid) + "-" + name.replace(" ", "_"))
	plt.close()

