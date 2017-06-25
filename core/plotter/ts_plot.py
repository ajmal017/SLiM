import pandas as pd 
import matplotlib.pylab as plt
import numpy as np
import os
from datetime import datetime

## sma plot
def plot_sma_symbol(symbol, date, price_from = 'Close', short_sma = True, long_sma = False):
	print "plot sma on {0}".format(symbol)
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print "price file not exists"
		return
	data = pd.read_csv(fn)
	price = np.array(data[price_from])
	ts = price[::-1]
	# d = range(len(ts))
	d = map(lambda x: datetime.strptime(x, "%d-%b-%y"), list(data.iloc[:,0])[::-1])

	path_ = 'data/price/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn_short = "data/plot/{0}/{0}_short_sma_{1}_{2}.png".format(date, symbol, price_from)
	fn_long = "data/plot/{0}/{0}_long_sma_{1}_{2}.png".format(date, symbol, price_from)
	if short_sma and not os.path.exists(fn_short):
		plt.clf()		
		sma_10 = pd.rolling_mean(ts, window = 10)
		sma_20 = pd.rolling_mean(ts, window = 20)
		sma_50 = pd.rolling_mean(ts, window = 50)
		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, sma_10, color = 'blue', label = 'sma 10')
		l3, = plt.plot(d, sma_20, color = 'red', label = 'sma 20')
		l4, = plt.plot(d, sma_50, color = 'green', label = 'sma 50')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.legend([l1, l2, l3, l4], loc = 0)
		plt.title("short sma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_short)
		# return
	if long_sma and not os.path.exists(fn_long):
		plt.clf()
		sma_10 = pd.rolling_mean(ts, window = 50)
		sma_20 = pd.rolling_mean(ts, window = 200)
		
		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, sma_10, color = 'blue', label = 'sma 50')
		l3, = plt.plot(d, sma_20, color = 'red', label = 'sma 200')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.legend(loc = 0)
		plt.title("long sma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_long)
		# return

## ewma plot
def plot_ewma_symbol(symbol, date, price_from, short_ewma = True, long_ewma = False, reverse = True, slot = None):
	print "plot ewma on {0}".format(symbol)
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print "price file not exists"
		return
	data = pd.read_csv(fn)
	price = np.array(data[price_from])
	if reverse:
		ts = price[::-1]
		# d = range(len(ts))
		d = map(lambda x: datetime.strptime(x, "%d-%b-%y"), list(data.iloc[:,0])[::-1])
		fn_short = "data/plot/{0}/{0}_short_ewma_{1}_{2}.png".format(date, symbol, price_from)
		fn_long = "data/plot/{0}/{0}_long_ewma_{1}_{2}.png".format(date, symbol, price_from)
	else:
		ts = price[slot[0]:slot[1]]
		d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0][slot[0]:slot[1]]))
		fn_short = "data/plot/{0}/{0}_short_ewma_{1}_{2}_{3}_{4}.png".format(date, symbol, price_from, slot[0], slot[1])
		fn_long = "data/plot/{0}/{0}_long_ewma_{1}_{2}.png".format(date, symbol, price_from)

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	
	if short_ewma and not os.path.exists(fn_short):
		plt.clf()
		ewma_10 = pd.ewma(ts, span = 10, adjust = False)
		ewma_20 = pd.ewma(ts, span = 20, adjust = False)
		ewma_50 = pd.ewma(ts, span = 50, adjust = False)
		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, ewma_10, color = 'blue', label = 'ewma 10')
		l3, = plt.plot(d, ewma_20, color = 'red', label = 'ewma 20')
		l4, = plt.plot(d, ewma_50, color = 'green', label = 'ewma 50')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.legend(loc = 0)
		plt.title("short ewma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_short)
		# return
	if long_ewma and not os.path.exists(fn_long):
		plt.clf()
		ewma_50 = pd.ewma(ts, span = 50, adjust = False)
		ewma_200 = pd.ewma(ts, span = 200, adjust = False)

		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, ewma_50, color = 'blue', label = 'ewma 50')
		l3, = plt.plot(d, ewma_200, color = 'red', label = 'ewma 200')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.legend(loc = 0)
		plt.title("long ewma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_long)

def plot_ma_symbol_list(symbol_source, date, price_from):
	## symbol_source: tech, health
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		# plot_sma_symbol(symbol, date)
		plot_ewma_symbol(symbol, date, price_from)

def img2html_symbol_list(symbol_source, date, type_, price_from):
	# type_: short_sma, short_ewma, long_sma, long_ewma
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	title = '{0}_{1}_{2}_{3}'.format(symbol_source, type_, price_from, date)
	fn = 'report/{0}.html'.format(title)

	with open(fn, 'w') as f:
		f.write('<!DOCTYPE html>\n')
		f.write('<html><head><title>{0}</title></head><body><center>\n'.format(title))
		for symbol in symbol_list:
			f.write('<h2>{0}</h2>\n'.format(symbol))
			f.write('<img src="../data/plot/{0}/{0}_{1}_{2}_{3}.png">\n'.format(date, type_, symbol, price_from))

		f.write('</center></body></html>')
	print("report saving to {0}".format(fn))

def plot_volume_symbol(symbol, date):
	print "plot volume on {0}".format(symbol)
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print "price file not exists"
		return
		
	window = 90
	data = pd.read_csv(fn)
	vol = np.array(data['Volume'][:window])
	ts = vol[::-1]
	d = map(lambda x: datetime.strptime(x, "%d-%b-%y"), list(data.iloc[:window,0])[::-1])

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn = "data/plot/{0}/{0}_{1}_volume.png".format(date, symbol)

	if not os.path.exists(fn):
		plt.clf()
		plt.bar(d, ts, color = 'b', label = 'volume')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.legend(loc = 0)
		plt.title("Volume plot for {0} on {1} (Recent {2} days)".format(symbol, date, window))
		plt.savefig(fn)


if __name__ == '__main__':
	symbol = 'GOOG'
	
	# date = '05_18'
	# date = datetime.now().strftime("%m_%d") # today

	# plot_sma_symbol(symbol = symbol, date = date, short_sma = True, long_sma = True)
	plot_ewma_symbol(symbol = symbol, date = 'history', price_from = 'Close', reverse = False, slot = [200,700])
	
	# plot_ma_symbol_list('watch', date)
	# plot_ma_symbol_list('bull_0406', date)
	# img2html_symbol_list('big_bull_0406', date, type_ = 'short_ewma')
	# img2html_symbol_list('hold', date, type_ = 'short_ewma')

	# plot_volume_symbol(symbol, date)


	