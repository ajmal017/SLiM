import pandas as pd 
import matplotlib.pylab as plt
import numpy as np
import os
from datetime import datetime
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def prep_data(symbol, __date = None):
	if not __date:
		__date = datetime.strftime(datetime.now(), '%m_%d')
		
	fn = 'data/price/{0}/{1}.csv'.format(__date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return None
	
	out_fil = 'data/strat/{}_data.csv'.format(symbol)

	data = pd.read_csv(fn)
	# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0]))
	x = list(data.iloc[:,0])
	d = np.arange(len(x))
	
	### get price and volume
	date = np.array(x)  ## from old to new
	price = np.array(data['Close'])
	vol = np.array(data['Volume'])
	
	### calculate ewma
	# ewma_5 = pd.ewma(price, span = 5, adjust = False)
	# ewma_10 = pd.ewma(price, span = 10, adjust = False)
	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	ewma_50 = pd.ewma(price, span = 50, adjust = False)
	ewma_200 = pd.ewma(price, span = 200, adjust = False)

	### calculate RSI
	delta = np.array(price[:-1]) - np.array(price[1:]) ## prev - now
	up = np.array([-c if c<0 else 0 for c in delta])
	down = np.array([c if c>0 else 0 for c in delta])
	
	ewma_up_14 = pd.ewma(up, span = 14, adjust = False)
	ewma_down_14 = pd.ewma(down, span = 14, adjust = False)
	rs_14 = ewma_up_14/ewma_down_14
	rsi_14 = 100 - 100 / (1 + rs_14)

	df_rsi = np.array(rsi_14).reshape(-1,1)
	
	df = np.concatenate([date.reshape(-1,1),
						price.reshape(-1,1),
						vol.reshape(-1,1), 
						# ewma_5.reshape(-1,1), 
						# ewma_10.reshape(-1,1), 
						ewma_20.reshape(-1,1), 
						ewma_50.reshape(-1,1), 
						ewma_200.reshape(-1,1)], axis = 1)[1:, :]

	cols = ['date', 'price', 'volume', 
			# 'ewma_5', 'ewma_10', 
			'ewma_20', 'ewma_50', 'ewma_200', 
			'rsi']

	# print(len(price), len(ewma_200), len(rsi_14))
	output = pd.DataFrame(np.concatenate([df, df_rsi], axis = 1 ), columns = cols)
	# print(output.head())

	# output.to_csv(out_fil, index = None)
	# print("data has been prepared")
	return output

def strategy(input_data, strat = 1):
	'''
	Strategy-1:
		if enter rsi_over_buy then buy
		if enter rsi_over_sell then sell
		if leave rsi_over_sell then buy
		if leave rsi_over_buy then sell
	Strategy-2:
		if enter rsi_over_buy then buy
		if enter rsi_over_sell then sell 
	Strategy-3:
		if leave rsi_over_sell then buy
		if leave rsi_over_buy then sell
	'''
	if input_data is None:
		return None

	date = input_data['date']
	rsi = input_data['rsi']
	price = [ float(x) for x in input_data['price'] ]
	

	signal = ['' for l in range(len(date))]
	
	if strat == 1:
		head = 15
		rsi_over_buy = np.array([ float(i) > 70 for i in rsi ])
		rsi_over_sell = np.array([ float(j) < 30 for j in rsi ])

		for t in range(1, len(date)):
			## enter over sell
			if not rsi_over_sell[t-1] and rsi_over_sell[t]:
				signal[t] = 'sell'
			## enter over buy
			if not rsi_over_buy[t-1] and rsi_over_buy[t]:
				signal[t] = 'buy'
			# leave over buy
			if rsi_over_buy[t-1] and not rsi_over_buy[t]:
				signal[t] = 'sell'
			# leave over sell
			if rsi_over_sell[t-1] and not rsi_over_sell[t]:
				signal[t] = 'buy'

	if strat == 2:
		head = 15
		rsi_over_buy = np.array([ float(i) > 70 for i in rsi ])
		rsi_over_sell = np.array([ float(j) < 30 for j in rsi ])

		for t in range(1, len(date)):
			## enter over sell
			if not rsi_over_sell[t-1] and rsi_over_sell[t]:
				signal[t] = 'sell'
			## enter over buy
			if not rsi_over_buy[t-1] and rsi_over_buy[t]:
				signal[t] = 'buy'

	if strat == 3:
		head = 15
		rsi_over_buy = np.array([ float(i) > 70 for i in rsi ])
		rsi_over_sell = np.array([ float(j) < 30 for j in rsi ])

		for t in range(1, len(date)):
			# leave over buy
			if rsi_over_buy[t-1] and not rsi_over_buy[t]:
				signal[t] = 'sell'
			# leave over sell
			if rsi_over_sell[t-1] and not rsi_over_sell[t]:
				signal[t] = 'buy'

	if strat == 4:
		head = 20
		ewma_20 = [ float(x) for x in input_data['ewma_20'] ]
		# ewma_50 = [ float(x) for x in input_data['ewma_50'] ]
		# ewma_200 = [ float(x) for x in input_data['ewma_200'] ]
		price_over_ewma20 = [ price[ind] > ewma_20[ind] for ind in range(len(date)) ]
		for t in range(1, len(date)):
			# down across ma20
			if price_over_ewma20[t-1] and not price_over_ewma20[t]:
				signal[t] = 'sell'
			# up across ma20
			if not price_over_ewma20[t-1] and price_over_ewma20[t]:
				signal[t] = 'buy'
	
	if strat == 5:
		head = 50
		ewma_50 = [ float(x) for x in input_data['ewma_50'] ]
		# ewma_200 = [ float(x) for x in input_data['ewma_200'] ]
		price_over_ewma50 = [ price[ind] > ewma_50[ind] for ind in range(len(date)) ]
		for t in range(1, len(date)):
			# down across ma50
			if price_over_ewma50[t-1] and not price_over_ewma50[t]:
				signal[t] = 'sell'
			# up across ma50
			if not price_over_ewma50[t-1] and price_over_ewma50[t]:
				signal[t] = 'buy'

	
	signal_data = pd.DataFrame({ 'date': date, 'price': price, 'signal': signal }).iloc[head:, :]
	# signal_data.to_csv(out_fil, index = None)

	### return date, price, signal
	return signal_data

def transaction(signal_data, symbol, strat):
	''' Goals: 
			to reduce transaction times
			to increase gain
			to reduce loss
		Actions:
			buy
			sell (sold out)
			add
			reduce
	'''
	if signal_data is None:
		return

	status = { "hold" : False, "price": 0 }
	earning = { "gain": 0, "loss": 0 }
	history = []

	for ind, row in signal_data.iterrows():
		signal = row['signal']
		if signal == 'buy':
			if status['hold'] == False:  ## buy if not hold
				status['hold'] = True
				status["price"] = row['price']
				history.append([row['date'], 'buy', row['price'], ''])
		if signal == 'sell':
			if status["hold"] == True:  ## sell if hold
				status['hold'] = False 
				diff = row['price'] - status["price"]
				if diff > 0:
					earning["gain"] += (diff / status["price"])
					history.append([row['date'], 'sell', row['price'], 'gain'])
				else:
					earning["loss"] += (-diff / status["price"])
					history.append([row['date'], 'sell', row['price'], 'loss'])

	df = pd.DataFrame(history, columns = ['date', 'act', 'price', 'g/l'])
	df.to_csv("data/strat/{}_history_{}.csv".format(symbol, strat), index = None)
	
	earning['loss'] = round(earning['loss']*100, 2)
	earning['gain'] = round(earning['gain']*100, 2)
	print(earning)
	print("transaction times: ", len(history)/2)


def run_strat_symbol(symbol, strat, _date = None):
	print("stock: {}".format(symbol))
	print("strategy: {}".format(strat))

	data = prep_data(symbol, __date = _date)

	rate = no_strategy(data)
	print("no str return: {}".format(rate))
	# beta = cal_beta(data, __date = _date)
	# print("beta: {}".format(beta))

	signal = strategy(data, strat)
	transaction(signal, symbol, strat)
	print("")


def run_strat_symbol_list(symbol_source, strat, date = None):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		run_strat_symbol(symbol, strat, _date = date)

def no_strategy(input_data):
	if input_data is None:
		return None
	price = list(input_data['price'])
	return round((float(price[-1]) - float(price[0])) / float(price[0]) * 100, 2)

def cal_beta(input_data, __date = None):
	if input_data is None:
		return None
	
	## get market data IXIC
	if not __date:
		__date = datetime.strftime(datetime.now(), '%m_%d')
	fn = 'data/price/{0}/^IXIC.csv'.format(__date)
	if not os.path.exists(fn):
		print("market data file not exists")
		return None
	market = pd.read_csv(fn)
	
	price = [float(i) for i in list(input_data['price']) ]
	market_price_all = list(market['Close'])
	diff = len(market_price_all) - len(price)
	market_price = market_price_all[diff:]
	ri = (np.array(price[1:]) - np.array(price[:-1])) / np.array(price[:-1])
	rm = (np.array(market_price[1:]) - np.array(market_price[:-1])) / np.array(market_price[:-1])

	beta = np.cov(ri, rm)[0][1] / np.var(rm)
	return round(beta,2)

if __name__ == '__main__':
	# d = data('ETH-USD')
	# symbol = 'AVGO'
	# strat = 3
	# run_strat_symbol(symbol, strat)

	run_strat_symbol_list("hold", 5, "05_08")
	