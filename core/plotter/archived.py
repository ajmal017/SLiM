## sma plot
# def plot_sma_symbol(symbol, date, price_from = 'Close', short_sma = False, long_sma = True):
# 	print "plot sma on {0}".format(symbol)
# 	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
# 	if not os.path.exists(fn):
# 		print "price file not exists"
# 		return
# 	data = pd.read_csv(fn)
# 	price = np.array(data[price_from])
# 	ts = price[::-1]
# 	# d = range(len(ts))
# 	d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0])[::-1])

# 	path_ = 'data/price/{0}'.format(date)
# 	if not os.path.exists(path_):
# 		os.mkdir(path_)
# 	fn_short = "data/plot/{0}/{0}_short_sma_{1}_{2}.png".format(date, symbol, price_from)
# 	fn_long = "data/plot/{0}/{0}_long_sma_{1}_{2}.png".format(date, symbol, price_from)
# 	if short_sma and not os.path.exists(fn_short):
# 		plt.clf()		
# 		sma_10 = pd.rolling_mean(ts, window = 10)
# 		sma_20 = pd.rolling_mean(ts, window = 20)
# 		sma_50 = pd.rolling_mean(ts, window = 50)
# 		l1, = plt.plot(d, ts, color = 'black', label = 'price')
# 		l2, = plt.plot(d, sma_10, color = 'blue', label = 'sma 10')
# 		l3, = plt.plot(d, sma_20, color = 'red', label = 'sma 20')
# 		l4, = plt.plot(d, sma_50, color = 'green', label = 'sma 50')
# 		x1,x2,y1,y2 = plt.axis()
# 		plt.axis((x1, x2 + 15, y1, y2))
# 		plt.legend([l1, l2, l3, l4], loc = 0)
# 		plt.title("short sma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
# 		plt.savefig(fn_short)
# 		# return
# 	if long_sma and not os.path.exists(fn_long):
# 		plt.clf()
# 		sma_10 = pd.rolling_mean(ts, window = 50)
# 		sma_20 = pd.rolling_mean(ts, window = 200)
		
# 		l1, = plt.plot(d, ts, color = 'black', label = 'price')
# 		l2, = plt.plot(d, sma_10, color = 'blue', label = 'sma 50')
# 		l3, = plt.plot(d, sma_20, color = 'red', label = 'sma 200')
# 		x1,x2,y1,y2 = plt.axis()
# 		plt.axis((x1, x2 + 15, y1, y2))
# 		plt.legend(loc = 0)
# 		plt.title("long sma(price: {2}) plot for {0} on {1}".format(symbol, date, price_from))
# 		plt.savefig(fn_long)
# 		# return


# def plot_volume_symbol(symbol, date):
# 	print "plot volume on {0}".format(symbol)
# 	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
# 	if not os.path.exists(fn):
# 		print "price file not exists"
# 		return
		
# 	window = 90
# 	data = pd.read_csv(fn)
# 	vol = np.array(data['Volume'][:window])
# 	ts = vol[::-1]
# 	d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:window,0])[::-1])

# 	path_ = 'data/plot/{0}'.format(date)
	
# 	if not os.path.exists(path_):
# 		os.mkdir(path_)
# 	fn = "data/plot/{0}/{0}_{1}_volume.png".format(date, symbol)
	
# 	if os.path.exists(fn):
# 		print "plot file exists"
# 		return

# 	if not os.path.exists(fn):
# 		plt.clf()
# 		plt.bar(d, ts, color = 'b', label = 'volume')
# 		x1,x2,y1,y2 = plt.axis()
# 		plt.axis((x1, x2 + 15, y1, y2))
# 		plt.legend(loc = 0)
# 		plt.title("Volume plot for {0} on {1} (Recent {2} days)".format(symbol, date, window))
# 		plt.savefig(fn)
