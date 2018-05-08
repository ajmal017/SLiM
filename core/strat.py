import pandas as pd 
import matplotlib.pylab as plt
import numpy as np
import os
from datetime import datetime


def data(symbol, date = None):
	if not date:
		date = datetime.strftime(datetime.now(), '%m_%d')
		
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print("price file not exists")
		return
	
	data = pd.read_csv(fn)
	# d = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), list(data.iloc[:,0]))
	x = list(data.iloc[:,0])
	d = np.arange(len(x))
	
	
	### get price and volume
	date = np.array(x)  ## from old to new
	price = np.array(data['Close'])
	vol = np.array(data['Volume'])
	
	### calculate ewma
	ewma_5 = pd.ewma(price, span = 5, adjust = False)
	ewma_10 = pd.ewma(price, span = 10, adjust = False)
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
						ewma_5.reshape(-1,1), 
						ewma_10.reshape(-1,1), 
						ewma_20.reshape(-1,1), 
						ewma_50.reshape(-1,1), 
						ewma_200.reshape(-1,1)], axis = 1)[1:, :]

	cols = ['date', 'price', 'volume', 'ewma_5', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_200', 'rsi']
	# print(len(price), len(ewma_200), len(rsi_14))
	output = pd.DataFrame(np.concatenate([df, df_rsi], axis = 1 ), columns = cols)
	# print(output.head())
	output.to_csv('{}_data.csv'.format(symbol), index = None)
	# return output

def strategy_1(symbol):
	''' Strategy:
		if enter rsi_over_buy: buy
		if enter rsi_over_sell: sell
		if leave rsi_over_buy: sell
		if leave rsi_over_sell: buy

	'''
	fn = 'data/strat/{0}_data.csv'.format(symbol)
	if not os.path.exists(fn):
		print("data file not exists")
		return
	
	input_data = pd.read_csv(fn)

	date = input_data['date']
	rsi = input_data['rsi']
	price = [ float(x) for x in input_data['price'] ]
	# ewma_20 = [ float(x) for x in input_data['ewma_20'] ]
	# ewma_50 = [ float(x) for x in input_data['ewma_50'] ]
	# ewma_200 = [ float(x) for x in input_data['ewma_200'] ]

	rsi_over_buy = np.array([ float(i) > 70 for i in rsi ])
	rsi_over_sell = np.array([ float(j) < 30 for j in rsi ])
	# rsi_safe = np.array([ float(k) <= 70 and float(k)>=30 for k in rsi ])
	
	signal = ['' for l in range(len(date))]
	
	for t in range(1, len(date)):
		## enter over sell
		if not rsi_over_sell[t-1] and rsi_over_sell[t]:
			signal[t] = 'sell'
		## enter over buy
		if not rsi_over_buy[t-1] and rsi_over_buy[t]:
			signal[t] = 'buy'
		
		## leave over buy
		if rsi_over_buy[t-1] and not rsi_over_buy[t]:
			signal[t] = 'sell'
		## leave over sell
		if rsi_over_sell[t-1] and not rsi_over_sell[t]:
			signal[t] = 'buy'


	df = pd.DataFrame({ 'date': date, 'price': price, 'signal': signal }).iloc[15:, :]
	df.to_csv('data/strat/{}_signal_1.csv'.format(symbol), index = None)
	
	# price_over_ewma20 = [ price[ind] > ewma_20[ind] for ind in range(len(date)) ]

	### return date, price, signal

def transaction(symbol, strat = 1):
	''' Goal: 
			to reduce transaction times
			to increase gain
			to reduce loss 
	'''
	fn = 'data/strat/{0}_signal_{1}.csv'.format(symbol, strat)
	if not os.path.exists(fn):
		print("signal file not exists")
		return
	
	signal_data = pd.read_csv(fn)

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
					earning["loss"] += (-diff / status["price"], 'loss')
				

	df = pd.DataFrame(history, columns = ['date', 'act', 'price'])
	df.to_csv("data/strat/{}_history_{}.csv".format(symbol, strat), index = None)
	
	print(earning)
	print("transaction times: ", len(history)/2)


if __name__ == '__main__':
	# d = data('ETH-USD')
	symbol = 'AVGO'
	data(symbol)
	sig = strategy(symbol)
	transaction(symbol)