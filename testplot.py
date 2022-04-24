import datetime as dt


def Average(lst):
   return sum(lst) / len(lst)


dates = ['2021/04/15', '2021/04/16', '2021/04/17', '2021/04/18', '2021/04/19', '2021/04/20', '2021/04/21', '2021/04/22', '2021/04/23', '2021/04/24', '2021/04/25', '2021/04/26', '2021/04/27', '2021/04/28', '2021/04/29', '2021/04/30', '2021/05/01', '2021/05/02', '2021/05/03', '2021/05/04', '2021/05/05', '2021/05/06', '2021/05/07', '2021/05/08', '2021/05/09', '2021/05/10', '2021/05/11', '2021/05/12', '2021/05/13', '2021/05/14']





x = [dt.datetime.strptime(d,'%Y/%m/%d').date() for d in dates]
y = range(len(x)) # many thanks to Kyss Tao for setting me straight here



n2021 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 3, 4, 2, 4, 7, 2, 6, 5, 5, 3, 3, 4, 8, 4, 2, 7, 4, 6]
n2020 = [1, 1, 1, 1, 2, 1, 2, 1, 4, 2, 2, 3, 2, 0, 2, 3, 4, 3, 6, 2, 4, 5, 3, 5, 4, 5, 3, 6, 5, 4]
n2019 = [0, 0, 0, 1, 0, 1, 1, 0, 2, 0, 4, 4, 6, 3, 2, 1, 1, 0, 1, 1, 2, 0, 2, 2, 7, 6, 3, 7, 6, 6]
n2018 = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 1, 2, 1, 2, 2, 3, 2, 3, 4, 4, 3, 2, 2, 4, 3, 2, 3]

n2021avg = []
n2020avg = []
n2019avg = []
n2018avg = []

for i in range(len(n2021)):
	start = i - 3
	if start < 0:
		start = 0

	end = i + 4
	if end > len(n2021)-1:
		end = len(n2021)-1

	n2021avg.append(Average(n2021[start:end]))
	n2020avg.append(Average(n2020[start:end]))
	n2019avg.append(Average(n2019[start:end]))
	n2018avg.append(Average(n2018[start:end]))


print(n2021avg)
print(n2020avg)
print(n2019avg)
print(n2018avg)


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
plt.plot(x,n2018avg, label = 2018)
plt.plot(x,n2019avg, label = 2019)
plt.plot(x,n2020avg, label = 2020)
plt.plot(x,n2021avg, label = 2021)
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()

