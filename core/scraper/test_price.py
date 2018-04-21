import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame, read_csv
import glob
import time
import numpy as np
import os.path
import urllib
from datetime import datetime, timedelta
import pandas_datareader.data as web
import matplotlib.pylab as plt


def scrape_price_symbol(symbol, source, year_range = (0, 3), override = True):

	print("---------- scraping price " + symbol)

	_today = datetime.today()
	end_date = _today - timedelta(365 * year_range[0])
	start_date = _today - timedelta(365 * year_range[1])

	path_ = 'data/price/test'

	if not os.path.exists(path_):
		os.mkdir(path_)
	fn = '{0}/{1}.csv'.format(path_, symbol)

	if not override and os.path.exists(fn):
		print("file exists")
		return

	try:
		data = web.DataReader(symbol, source, start_date, end_date)
		data.to_csv(fn)
		print("successfully saved to " + fn)
	except:
		print("error: download failed")


def plot_price_volume_symbol(symbol, override = True):

	fn = 'data/price/test/{}.csv'.format(symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return

	print("plot ewma + volume on {0}".format(symbol))

	path_ = 'data/plot/test'
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn_fig = "data/plot/test/{0}_ewma_volume.png".format(symbol)

	if not override and os.path.exists(fn_fig):
		print("file exists")
		return

	data = pd.read_csv(fn)
	x = list(data.iloc[:,0])
	d = np.arange(len(x))
	xspace = int(len(x) / 5)
	if xspace == 0:
		print("data not enough")
		return
	price = np.array(data['Close'])
	vol = np.array(data['Volume'])

	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	ewma_50 = pd.ewma(price, span = 50, adjust = False)
	ewma_200 = pd.ewma(price, span = 200, adjust = False)

	plt.clf()
	ax1 = plt.gca()
	l1 = ax1.plot(d, price, color = 'black', label = 'price')
	l2 = ax1.plot(d, ewma_20, color = 'blue', label = 'ewma 20')
	l3 = ax1.plot(d, ewma_50, color = 'red', label = 'ewma 50')
	l4 = ax1.plot(d, ewma_200, color = 'green', label = 'ewma 200')
	ax2 = ax1.twinx()
	v1 = ax2.bar(d, vol, color = 'b', label = 'volume')
	x1, x2, y3, y4 = ax2.axis()
	ax2.axis((x1, x2, y3, 5*y4))

	plt.xticks(d[::xspace], x[::xspace], fontsize = 1)
	plt.setp(plt.gca().get_xticklabels(), rotation = 90, horizontalalignment = 'right')
	lns = l1+l2+l3+l4
	plt.legend(lns, [l.get_label() for l in lns], loc = 2, prop = {'size': 10})
	plt.title("price + ewma + volume plot for {0}".format(symbol))
	plt.savefig(fn_fig, dpi = 500)


def test(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		scrape_price_symbol(symbol = symbol, source = 'yahoo', year_range = (1, 4))
		plot_price_volume_symbol(symbol)


if __name__ == '__main__':
	test("watch")