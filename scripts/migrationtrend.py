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
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# Get current directory
path = os.getcwd()
# Parent directory
parent = os.path.dirname(path)
sys.path.insert(0,parent)
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


def divide_chunks(l, n):
	# looping till length l
	for i in range(0, len(l), n): 
		yield l[i:i + n]

def GetSpeciesPlot(year_start, year_end, month_start, month_end, speciesid, name):


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
		link  = "https://old.waarneming.nl/soort/maps/"+str(speciesid)+"?from=" + date1.strftime('%Y/%m/%d') + "&to=" + date2.strftime('%Y/%m/%d')
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
	yy = list(divide_chunks(y, len(x_axis)))

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
		plt.plot(X_axis, yyy, label = str(year),  alpha=0.5, linestyle='dashed')
	plt.plot(X_axis, yy_mean, color="black", label = "gem.")

	plt.gca().set_ylim(bottom=0)
	plt.gca().set_xlim(left=0, right=len(x_axis)-1)

	plt.xticks(X_axis, x_axis)
	plt.gca().xaxis.set_major_locator(majorLocator)
	plt.gca().xaxis.set_minor_locator(minorLocator)

	plt.title(name)
	plt.legend()
	plt.savefig(str(speciesid) + "-" + name)
	plt.close()
	#plt.show()


#GetSpeciesPlot(2021,2022, 10, 12, 781, "Zwarte Rotgans")

GetSpeciesPlot(2018,2023, 1, 12, 781,   "Zwarte Rotgans")
GetSpeciesPlot(2018,2023, 1, 12, 769,   "Witbuikrotgans")
GetSpeciesPlot(2018,2023, 1, 12, 313,   "Roodhalsgans")
GetSpeciesPlot(2018,2023, 1, 12, 327,   "Sneeuwgans")
GetSpeciesPlot(2018,2023, 1, 12, 338,   "Taigarietgans")
GetSpeciesPlot(2018,2023, 1, 12, 244,   "Dwerggans")
GetSpeciesPlot(2018,2023, 1, 12, 772,   "Witoogeend")
GetSpeciesPlot(2018,2023, 1, 12, 264,   "Ijseend")
GetSpeciesPlot(2018,2023, 1, 12, 216,   "Alpengierzwaluw")
GetSpeciesPlot(2018,2023, 1, 12, 18,    "Kwartelkoning")
GetSpeciesPlot(2018,2023, 1, 12, 17,    "Porseleinhoen")
GetSpeciesPlot(2018,2023, 1, 12, 19,    "Kraanvogel")
GetSpeciesPlot(2018,2023, 1, 12, 1401,  "Flamingo")
GetSpeciesPlot(2018,2023, 1, 12, 332, 	"Steltkluut")
GetSpeciesPlot(2018,2023, 1, 12, 294, 	"Morinelplevier")
GetSpeciesPlot(2018,2023, 1, 12, 905, 	"Breedbekstrandloper")
GetSpeciesPlot(2018,2023, 1, 12, 370, 	"Gestreepte strandloper")
GetSpeciesPlot(2018,2023, 1, 12, 253, 	"Grauwe franjepoot")
GetSpeciesPlot(2018,2023, 1, 12, 318, 	"Rosse franjepoot")
GetSpeciesPlot(2018,2023, 1, 12, 307, 	"Poelruiter")
GetSpeciesPlot(2018,2023, 1, 12, 1387,  "Vorkstaartmeeuw")
GetSpeciesPlot(2018,2023, 1, 12, 255,   "Grote burgemeester")
GetSpeciesPlot(2018,2023, 1, 12, 272,   "Kleine burgemeester")
GetSpeciesPlot(2018,2023, 1, 12, 368,   "Lachstern")
GetSpeciesPlot(2018,2023, 1, 12, 762,   "Witwangstern")
GetSpeciesPlot(2018,2023, 1, 12, 361,   "Witvleugelstern")
GetSpeciesPlot(2018,2023, 1, 12, 278,   "Kleinste Jager")
GetSpeciesPlot(2018,2023, 1, 12, 270,   "Kleine alk")
GetSpeciesPlot(2018,2023, 1, 12, 1538,  "Zwarte zeekoet")
GetSpeciesPlot(2018,2023, 1, 12, 304,   "Papegaaiduiker")
GetSpeciesPlot(2018,2023, 1, 12, 263,   "Ijsduiker")
GetSpeciesPlot(2018,2023, 1, 12, 335,   "Stormvogeltje")
GetSpeciesPlot(2018,2023, 1, 12, 369,   "Vale pijlstormvogel")
GetSpeciesPlot(2018,2023, 1, 12, 362,   "Zwarte ooievaar")
GetSpeciesPlot(2018,2023, 1, 12, 285,   "Kuifaalscholver")
GetSpeciesPlot(2018,2023, 1, 12, 853,   "Zwarte Ibis")
GetSpeciesPlot(2018,2023, 1, 12, 4, 	"Woudaap")
GetSpeciesPlot(2018,2023, 1, 12, 5, 	"Kwak")
GetSpeciesPlot(2018,2023, 1, 12, 360, 	"Koereiger")
GetSpeciesPlot(2018,2023, 1, 12, 324, 	"Slangenarend")
GetSpeciesPlot(2018,2023, 1, 12, 334, 	"Steppekiekendief")
GetSpeciesPlot(2018,2023, 1, 12, 321, 	"Ruigpootbuizerd")
GetSpeciesPlot(2018,2023, 1, 12, 38, 	"Hop")
GetSpeciesPlot(2018,2023, 1, 12, 300, 	"Oehoe")
GetSpeciesPlot(2018,2023, 1, 12, 1386,  "Bijeneter")
GetSpeciesPlot(2018,2023, 1, 12, 39, 	"Draaihals")
GetSpeciesPlot(2018,2023, 1, 12, 290, 	"Middelste bonte specht")
GetSpeciesPlot(2018,2023, 1, 12, 316, 	"Roodpootvalk")
GetSpeciesPlot(2018,2023, 1, 12, 53, 	"Roodkopklauwier")
GetSpeciesPlot(2018,2023, 1, 12, 67, 	"Bonte kraai")
GetSpeciesPlot(2018,2023, 1, 12, 306, 	"Pestvogel")
GetSpeciesPlot(2018,2023, 1, 12, 1007,  "Roodstuitzwaluw")
GetSpeciesPlot(2018,2023, 1, 12, 262, 	"Hume's bladkoning")
GetSpeciesPlot(2018,2023, 1, 12, 227, 	"Bladkoning")
GetSpeciesPlot(2018,2023, 1, 12, 303, 	"Pallas' boszanger")
GetSpeciesPlot(2018,2023, 1, 12, 1503,  "Bruine boszanger")
GetSpeciesPlot(2018,2023, 1, 12, 765, 	"Siberische tjiftjaf")
GetSpeciesPlot(2018,2023, 1, 12, 252, 	"Grauwe fitis")
GetSpeciesPlot(2018,2023, 1, 12, 49, 	"Grote karekiet")
GetSpeciesPlot(2018,2023, 1, 12, 1129,  "Waterrietzanger")
GetSpeciesPlot(2018,2023, 1, 12, 1123,  "Struikrietzanger")
GetSpeciesPlot(2018,2023, 1, 12, 302, 	"Orpheusspotvogel")
GetSpeciesPlot(2018,2023, 1, 12, 1115,  "Krekelzanger")
GetSpeciesPlot(2018,2023, 1, 12, 1111,  "Graszanger")
GetSpeciesPlot(2018,2023, 1, 12, 371, 	"Sperwergrasmus")
GetSpeciesPlot(2018,2023, 1, 12, 80485, "Taigaboomkruiper ssp familiaris")
GetSpeciesPlot(2018,2023, 1, 12, 199294,"Roze spreeuw")
GetSpeciesPlot(2018,2023, 1, 12, 1182,  "Kleine vliegenvanger")
GetSpeciesPlot(2018,2023, 1, 12, 1561,  "Blauwsaart")
GetSpeciesPlot(2018,2023, 1, 12, 84884, "Waterspreeuw")
GetSpeciesPlot(2018,2023, 1, 12, 239,   "Citroenkwikstaart")
GetSpeciesPlot(2018,2023, 1, 12, 757,   "Grote pieper")
GetSpeciesPlot(2018,2023, 1, 12, 43,    "Duinpieper")
GetSpeciesPlot(2018,2023, 1, 12, 755,   "Roodkeelpieper")
GetSpeciesPlot(2018,2023, 1, 12, 315,   "Roodmus")
GetSpeciesPlot(2018,2023, 1, 12, 248,   "Europese kanarie")
GetSpeciesPlot(2018,2023, 1, 12, 57,    "Grauwe gors")
GetSpeciesPlot(2018,2023, 1, 12, 56,    "Ortolaan")
GetSpeciesPlot(2018,2023, 1, 12, 245,   "Dwerggors")
GetSpeciesPlot(2018,2023, 1, 12, 1529,  "Bosgors")
