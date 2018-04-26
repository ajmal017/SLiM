import pandas as pd 
import matplotlib.pylab as plt
import numpy as np
import os
from datetime import datetime
from shutil import copyfile


## ewma plot
def plot_ewma_symbol(symbol, date, price_from, short_ewma = False, long_ewma = True, reverse = False, slot = None):
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return
	data = pd.read_csv(fn)
	price = np.array(data[price_from])
	if reverse:
		ts = price[::-1]
		d = range(len(ts))
		x = list(data.iloc[:,0])[::-1]
		# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0])[::-1])
		fn_short = "data/plot/{0}/{0}_short_ewma_{1}_{2}.png".format(date, symbol, price_from)
		fn_long = "data/plot/{0}/{0}_long_ewma_{1}_{2}.png".format(date, symbol, price_from)
	else:
		# ts = price[slot[0]:slot[1]]
		ts = price
		d = range(len(ts))
		x = list(data.iloc[:,0])
		# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0][slot[0]:slot[1]]))
		# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0]))
		fn_short = "data/plot/{0}/{0}_short_ewma_{1}_{2}.png".format(date, symbol, price_from)
		fn_long = "data/plot/{0}/{0}_long_ewma_{1}_{2}.png".format(date, symbol, price_from)

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	
	if short_ewma and not os.path.exists(fn_short):
		print("plot short ewma on {0}".format(symbol))

		plt.clf()
		ewma_10 = pd.ewma(ts, span = 10, adjust = False)
		ewma_20 = pd.ewma(ts, span = 20, adjust = False)
		ewma_50 = pd.ewma(ts, span = 50, adjust = False)
		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, ewma_10, color = 'blue', label = 'ewma 10')
		l3, = plt.plot(d, ewma_20, color = 'red', label = 'ewma 20')
		l4, = plt.plot(d, ewma_50, color = 'green', label = 'ewma 50')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2, y1, y2))
		plt.xticks(d[::30], x[::30])
		plt.legend(loc = 0)
		plt.title("short ewma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_short)
		# return
	if long_ewma and not os.path.exists(fn_long):
		print("plot long ewma on {0}".format(symbol))

		plt.clf()
		ewma_50 = pd.ewma(ts, span = 50, adjust = False)
		ewma_200 = pd.ewma(ts, span = 200, adjust = False)

		l1, = plt.plot(d, ts, color = 'black', label = 'price')
		l2, = plt.plot(d, ewma_50, color = 'blue', label = 'ewma 50')
		l3, = plt.plot(d, ewma_200, color = 'red', label = 'ewma 200')
		x1,x2,y1,y2 = plt.axis()
		plt.axis((x1, x2 + 15, y1, y2))
		plt.xticks(d[::30], x[::30])
		plt.legend(loc = 0)
		plt.title("long ewma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
		plt.savefig(fn_long)


def plot_ma_symbol_list(symbol_source, date, price_from):
	## symbol_source: tech, health
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		# plot_sma_symbol(symbol, date)
		plot_ewma_symbol(symbol, date, price_from)


def plot_price_volume_symbol(symbol, date, override):
	if not date:
		date = datetime.strftime(datetime.now(), '%m_%d')
		
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return

	print("plot ewma + volume on {0}".format(symbol))

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn_fig = "data/plot/{0}/{0}_ewma_volume_{1}.png".format(date, symbol)

	if not override and os.path.exists(fn_fig):
		print("file exists")
		return
	data = pd.read_csv(fn)
	# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0]))
	x = list(data.iloc[:,0])
	d = np.arange(len(x))
	xspace = int(len(x) / 10)
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
	# fig.tight_layout()
	plt.xticks(d[::xspace], x[::xspace], fontsize = 1)
	plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
	lns = l1+l2+l3+l4
	plt.legend(lns, [l.get_label() for l in lns], loc = 2, prop={'size': 10})
	plt.title("price + ewma + volume plot for {0} on {1}".format(symbol, date))
	plt.savefig(fn_fig, dpi = 500)
	# plt.show()

def plot_price_volume_crypto(symbol, date, override):
	if not date:
		date = datetime.strftime(datetime.now(), '%m_%d')
		
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return

	print("plot ewma + volume on {0}".format(symbol))

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn_fig = "data/plot/{0}/{0}_ewma_volume_{1}.png".format(date, symbol)

	if not override and os.path.exists(fn_fig):
		print("file exists")
		return
	data = pd.read_csv(fn)
	# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0]))
	x = list(data.iloc[:,0])
	d = np.arange(len(x))
	xspace = int(len(x) / 10)
	if xspace == 0:
		print("data not enough")
		return
	price = np.array(data['Close'])
	vol = np.array(data['Volume'])
	
	ewma_5 = pd.ewma(price, span = 5, adjust = False)
	ewma_10 = pd.ewma(price, span = 10, adjust = False)
	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	ewma_50 = pd.ewma(price, span = 50, adjust = False)
	ewma_200 = pd.ewma(price, span = 200, adjust = False)
	
	plt.clf()
	ax1 = plt.gca()
	l1 = ax1.plot(d, price, color = 'black', label = 'price')
	l2_1 = ax1.plot(d, ewma_5, color = 'pink', label = 'ewma 5')
	l2_2 = ax1.plot(d, ewma_10, color = 'purple', label = 'ewma 10')
	l2 = ax1.plot(d, ewma_20, color = 'blue', label = 'ewma 20')
	l3 = ax1.plot(d, ewma_50, color = 'red', label = 'ewma 50')
	l4 = ax1.plot(d, ewma_200, color = 'green', label = 'ewma 200')
	
	ax2 = ax1.twinx()
	v1 = ax2.bar(d, vol, color = 'b', label = 'volume')
	x1, x2, y3, y4 = ax2.axis()
	ax2.axis((x1, x2, y3, 5*y4))
	# fig.tight_layout()
	plt.xticks(d[::xspace], x[::xspace], fontsize = 1)
	plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
	lns = l1+l2_1+l2_2+l2+l3+l4
	plt.legend(lns, [l.get_label() for l in lns], loc = 2, prop={'size': 10})
	plt.title("price + ewma + volume plot for {0} on {1}".format(symbol, date))
	plt.savefig(fn_fig, dpi = 500)
	# plt.show()

def plot_rsi_symbol(symbol, date, override):
	if not date:
		date = datetime.strftime(datetime.now(), '%m_%d')

	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return
	print("plot rsi on {0}".format(symbol))

	path_ = 'data/plot/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	
	fn_fig = "data/plot/{0}/{0}_rsi_{1}.png".format(date, symbol)
	if not override and os.path.exists(fn_fig):
		print("file exists")
		return

	data = pd.read_csv(fn)
	price = data['Close']
	x = list(data.iloc[:,0])[1:]
	d = np.arange(len(x))
	xspace = int(len(x) / 10)
	delta = np.array(price[:-1]) - np.array(price[1:]) ## prev - now
	up = np.array([-x if x<0 else 0 for x in delta])
	down = np.array([x if x>0 else 0 for x in delta])
	
	ewma_up_15 = pd.ewma(up, span = 15, adjust = False)
	ewma_down_15 = pd.ewma(down, span = 15, adjust = False)
	rs_15 = ewma_up_15/ewma_down_15
	rsi_15 = 100 - 100 / (1 + rs_15)
	
	ewma_up_30 = pd.ewma(up, span = 30, adjust = False)
	ewma_down_30 = pd.ewma(down, span = 30, adjust = False)
	rs_30 = ewma_up_30/ewma_down_30
	rsi_30 = 100 - 100 / (1 + rs_30)

	plt.clf()
	# plt.figure(figsize=(12,8))
	plt.plot(d, rsi_15, label = '15 days')
	plt.plot(d, rsi_30, label = '30 days')
	plt.plot(d, np.ones(len(rsi_15))*70, color = 'green')
	plt.plot(d, np.ones(len(rsi_15))*30, color = 'green')
	plt.xticks(d[::xspace], x[::xspace], fontsize = 5)
	plt.legend()
	plt.title("15/30 Days RSI on {0} ".format(symbol))
	plt.savefig(fn_fig, dpi = 500)


def plot_price_volume_symbol_list(symbol_source, date, override = False):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		plot_price_volume_symbol(symbol, date, override)

def plot_rsi_symbol_list(symbol_source, date, override = False):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		plot_rsi_symbol(symbol, date, override)

if __name__ == '__main__':
	
	
	# date = '05_18'
	# date = datetime.now().strftime("%m_%d") # today

	# plot_ewma_symbol(symbol = symbol, date = 'history', price_from = 'Close', reverse = False, slot = [200,700])
	
	# plot_ma_symbol_list('watch', date)
	# img2html_symbol_list('big_bull_0406', date, type_ = 'short_ewma')
	# img2html_symbol_list('hold', date, type_ = 'short_ewma')

	# plot_price_volume_symbol("^IXIC", None, True)
	# plot_price_volume_crypto("BTC-USD", None, True)
	# plot_price_volume_crypto("ETH-USD", None, True)
	# plot_rsi_symbol("ETH-USD", None, 15, True)
	plot_rsi_symbol("BTC-USD", None, True)