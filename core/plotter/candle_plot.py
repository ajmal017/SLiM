from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
# import pandas.io.data as web
import matplotlib.dates as dates
import matplotlib.pylab as plt
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import os
from datetime import datetime

def pandas_candlestick_ohlc(dat, symbol, date, local = False, stick = "week", otherseries = None):
	"""
	:param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
	:param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
	:param otherseries: An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines
	This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
	"""
	
	plt.clf()
	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	dayFormatter = DateFormatter('%d')      # e.g., 12
	# Create a new DataFrame which includes OHLC data for each period specified by stick input
	transdat = dat.loc[:,["Open", "High", "Low", "Close"]]
	if (type(stick) == str):
		if stick == "day":
			plotdat = transdat
			stick = 1 # Used for plotting
		elif stick in ["week", "month", "year"]:
			if stick == "week":
				transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
			elif stick == "month":
				transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
			transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
			grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
			plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
			for name, group in grouped:
				plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
											"High": max(group.High),
											"Low": min(group.Low),
											"Close": group.iloc[-1,3]},
										   index = [group.index[0]]))
			if stick == "week": stick = 5
			elif stick == "month": stick = 30
			elif stick == "year": stick = 365
	elif (type(stick) == int and stick >= 1):
		transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
		grouped = transdat.groupby("stick")
		plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
		for name, group in grouped:
			plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
										"High": max(group.High),
										"Low": min(group.Low),
										"Close": group.iloc[-1,3]},
									   index = [group.index[0]]))
	else:
		raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')
	# Set plot parameters, including the axis object ax used for plotting
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	if (not local and plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days')) or (local and plotdat.index[-1] - plotdat.index[0] < 730):
	    weekFormatter = DateFormatter('%y-%m-%d')  # e.g., Jan 12
	    ax.xaxis.set_major_locator(mondays)
	    ax.xaxis.set_minor_locator(alldays)
	else:
	    weekFormatter = DateFormatter('%y-%m-%d')
	ax.xaxis.set_major_formatter(weekFormatter)
	ax.grid(True)

	# Create the candelstick chart
	if not local:
		candlestick_ohlc(ax, list(zip(list(dates.date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
					  plotdat["Low"].tolist(), plotdat["Close"].tolist())),
					  colorup = "black", colordown = "red", width = stick * .4)
	else:
		candlestick_ohlc(ax, list(zip(list(plotdat.index.tolist()), plotdat["Open"].tolist(), plotdat["High"].tolist(),
					  plotdat["Low"].tolist(), plotdat["Close"].tolist())),
					  colorup = "black", colordown = "red", width = stick * .4)
	# Plot other series (such as moving averages) as lines
	if otherseries != None:
		if type(otherseries) != list:
			otherseries = [otherseries]
		dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

	plt.title("{0} days candle plot for {1} on {2}".format(stick, symbol, date))
	fig_path = 'data/plot/{0}/{0}_candle_{1}.png'.format(date, symbol)
	plt.savefig(fig_path, dpi = 500)
	# plt.show()

def plot_candle_symbol(symbol, date, year_start = 2017, year_end =2018, step = 1):
	print("plot candle on {0}".format(symbol))
	
	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)

	fig_path = 'data/plot/{0}/{0}_candle_{1}.png'.format(date, symbol)
	# if os.path.exists(fig_path):
	# 	print("file exists")
	# 	return
	
	if step > 5:
		duration = 'month'
	elif step > 1:
		duration = 'week'
	else:
		duration = 'week'
		
	for year in range(year_start, year_end, step):
		print(year)
		start_date = datetime(year,1,1)
		end_date = datetime(year+step,1,1)
		dat = web.DataReader(symbol, 'yahoo', start_date, end_date)
		dat.to_csv("data/price/{0}_{1}.csv".format(symbol, date))
		pandas_candlestick_ohlc(dat, symbol, date, local = False, stick = duration, otherseries = None)

def plot_candle_symbol_list(symbol_source, date):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		plot_candle_symbol(symbol, date)


if __name__ == '__main__':
	# pass
	symbol = '^IXIC'
	plot_candle_symbol(symbol, 'long', year_start = 2017, year_end = 2018, step = 1)
	
	# symbol = 'NVDA'
	# plot_candle_symbol(symbol, 'short', year_start = 2017, year_end = 2018, step = 1)