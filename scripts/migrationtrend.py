#from BaseClass import *
#from MigClass import *
#import time
import datetime
from datetime import datetime as dt
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


	print("Working on :" + name)
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
		plt.plot(X_axis + 0.5, yyy, label = str(year),  alpha=0.5, linestyle='dashed')
	plt.plot(X_axis + 0.5, yy_mean, color="black", label = "gem.")

	plt.gca().set_ylim(bottom=0)
	plt.gca().set_xlim(left=0, right=len(x_axis))

	plt.xticks(X_axis, x_axis)
	plt.gca().xaxis.set_major_locator(majorLocator)
	plt.gca().xaxis.set_minor_locator(minorLocator)

	plt.title(name)
	plt.legend()
	plt.savefig(str(speciesid) + "-" + name)
	plt.close()
	#plt.show()


#GetSpeciesPlot(2021,2022, 1, 12, 781, "Zwarte Rotgans")
end_year = dt.now().year-1
start_year = end_year -5

#GetSpeciesPlot(start_year,end_year, 1, 12, 781,   "Zwarte Rotgans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 769,   "Witbuikrotgans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 313,   "Roodhalsgans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 327,   "Sneeuwgans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 338,   "Taigarietgans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 244,   "Dwerggans")
#GetSpeciesPlot(start_year,end_year, 1, 12, 772,   "Witoogeend")
#GetSpeciesPlot(start_year,end_year, 1, 12, 264,   "Ijseend")
#GetSpeciesPlot(start_year,end_year, 1, 12, 216,   "Alpengierzwaluw")
#GetSpeciesPlot(start_year,end_year, 1, 12, 18,    "Kwartelkoning")
#GetSpeciesPlot(start_year,end_year, 1, 12, 17,    "Porseleinhoen")
#GetSpeciesPlot(start_year,end_year, 1, 12, 19,    "Kraanvogel")
#GetSpeciesPlot(start_year,end_year, 1, 12, 1401,  "Flamingo")
#GetSpeciesPlot(start_year,end_year, 1, 12, 332, 	"Steltkluut")
#GetSpeciesPlot(start_year,end_year, 1, 12, 294, 	"Morinelplevier")
#GetSpeciesPlot(start_year,end_year, 1, 12, 905, 	"Breedbekstrandloper")
#GetSpeciesPlot(start_year,end_year, 1, 12, 370, 	"Gestreepte strandloper")
#GetSpeciesPlot(start_year,end_year, 1, 12, 253, 	"Grauwe franjepoot")
GetSpeciesPlot(start_year,end_year, 1, 12, 318, 	"Rosse franjepoot")
GetSpeciesPlot(start_year,end_year, 1, 12, 307, 	"Poelruiter")
GetSpeciesPlot(start_year,end_year, 1, 12, 1387,  "Vorkstaartmeeuw")
GetSpeciesPlot(start_year,end_year, 1, 12, 255,   "Grote burgemeester")
GetSpeciesPlot(start_year,end_year, 1, 12, 272,   "Kleine burgemeester")
GetSpeciesPlot(start_year,end_year, 1, 12, 368,   "Lachstern")
GetSpeciesPlot(start_year,end_year, 1, 12, 762,   "Witwangstern")
GetSpeciesPlot(start_year,end_year, 1, 12, 361,   "Witvleugelstern")
GetSpeciesPlot(start_year,end_year, 1, 12, 278,   "Kleinste Jager")
GetSpeciesPlot(start_year,end_year, 1, 12, 270,   "Kleine alk")
GetSpeciesPlot(start_year,end_year, 1, 12, 1538,  "Zwarte zeekoet")
GetSpeciesPlot(start_year,end_year, 1, 12, 304,   "Papegaaiduiker")
GetSpeciesPlot(start_year,end_year, 1, 12, 263,   "Ijsduiker")
GetSpeciesPlot(start_year,end_year, 1, 12, 335,   "Stormvogeltje")
GetSpeciesPlot(start_year,end_year, 1, 12, 369,   "Vale pijlstormvogel")
GetSpeciesPlot(start_year,end_year, 1, 12, 362,   "Zwarte ooievaar")
GetSpeciesPlot(start_year,end_year, 1, 12, 285,   "Kuifaalscholver")
GetSpeciesPlot(start_year,end_year, 1, 12, 853,   "Zwarte Ibis")
GetSpeciesPlot(start_year,end_year, 1, 12, 4, 	"Woudaap")
GetSpeciesPlot(start_year,end_year, 1, 12, 5, 	"Kwak")
GetSpeciesPlot(start_year,end_year, 1, 12, 360, 	"Koereiger")
GetSpeciesPlot(start_year,end_year, 1, 12, 324, 	"Slangenarend")
GetSpeciesPlot(start_year,end_year, 1, 12, 334, 	"Steppekiekendief")
GetSpeciesPlot(start_year,end_year, 1, 12, 321, 	"Ruigpootbuizerd")
GetSpeciesPlot(start_year,end_year, 1, 12, 38, 	"Hop")
GetSpeciesPlot(start_year,end_year, 1, 12, 300, 	"Oehoe")
GetSpeciesPlot(start_year,end_year, 1, 12, 1386,  "Bijeneter")
GetSpeciesPlot(start_year,end_year, 1, 12, 39, 	"Draaihals")
GetSpeciesPlot(start_year,end_year, 1, 12, 290, 	"Middelste bonte specht")
GetSpeciesPlot(start_year,end_year, 1, 12, 316, 	"Roodpootvalk")
GetSpeciesPlot(start_year,end_year, 1, 12, 53, 	"Roodkopklauwier")
GetSpeciesPlot(start_year,end_year, 1, 12, 67, 	"Bonte kraai")
GetSpeciesPlot(start_year,end_year, 1, 12, 306, 	"Pestvogel")
GetSpeciesPlot(start_year,end_year, 1, 12, 1007,  "Roodstuitzwaluw")
GetSpeciesPlot(start_year,end_year, 1, 12, 262, 	"Hume's bladkoning")
GetSpeciesPlot(start_year,end_year, 1, 12, 227, 	"Bladkoning")
GetSpeciesPlot(start_year,end_year, 1, 12, 303, 	"Pallas' boszanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 1503,  "Bruine boszanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 765, 	"Siberische tjiftjaf")
GetSpeciesPlot(start_year,end_year, 1, 12, 252, 	"Grauwe fitis")
GetSpeciesPlot(start_year,end_year, 1, 12, 49, 	"Grote karekiet")
GetSpeciesPlot(start_year,end_year, 1, 12, 1129,  "Waterrietzanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 1123,  "Struikrietzanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 302, 	"Orpheusspotvogel")
GetSpeciesPlot(start_year,end_year, 1, 12, 1115,  "Krekelzanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 1111,  "Graszanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 371, 	"Sperwergrasmus")
GetSpeciesPlot(start_year,end_year, 1, 12, 80485, "Taigaboomkruiper ssp familiaris")
GetSpeciesPlot(start_year,end_year, 1, 12, 199294,"Roze spreeuw")
GetSpeciesPlot(start_year,end_year, 1, 12, 1182,  "Kleine vliegenvanger")
GetSpeciesPlot(start_year,end_year, 1, 12, 1561,  "Blauwsaart")
GetSpeciesPlot(start_year,end_year, 1, 12, 84884, "Waterspreeuw")
GetSpeciesPlot(start_year,end_year, 1, 12, 239,   "Citroenkwikstaart")
GetSpeciesPlot(start_year,end_year, 1, 12, 757,   "Grote pieper")
GetSpeciesPlot(start_year,end_year, 1, 12, 43,    "Duinpieper")
GetSpeciesPlot(start_year,end_year, 1, 12, 755,   "Roodkeelpieper")
GetSpeciesPlot(start_year,end_year, 1, 12, 315,   "Roodmus")
GetSpeciesPlot(start_year,end_year, 1, 12, 248,   "Europese kanarie")
GetSpeciesPlot(start_year,end_year, 1, 12, 57,    "Grauwe gors")
GetSpeciesPlot(start_year,end_year, 1, 12, 56,    "Ortolaan")
GetSpeciesPlot(start_year,end_year, 1, 12, 245,   "Dwerggors")
GetSpeciesPlot(start_year,end_year, 1, 12, 1529,  "Bosgors")
