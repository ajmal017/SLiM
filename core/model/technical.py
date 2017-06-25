import pandas as pd
from pandas import DataFrame, read_csv
import glob
import time
import numpy as np
import os.path
from datetime import datetime

def cal_technical_indicators_symbol(symbol, date, silent = True):
	fn = "data/price/{0}/{1}.csv".format(date, symbol)
	if not os.path.exists(fn):
		print "error: no price file exists {0} {1}".format(symbol, date)
		return
	data = pd.read_csv(fn)
	close_price = data['Close']
	i = 0
	x = data.iloc[i,0]
	sma_10 = np.mean(close_price[i:10+i])
	sma_20 = np.mean(close_price[i:20+i])
	sma_50 = np.mean(close_price[i:50+i])
	sma_100 = np.mean(close_price[i:100+i])
	# if i+200< len(close_price):
	sma_200 = np.mean(close_price[i:200+i])
	current_price = close_price[0]
	if not silent:
		print "----- technical indicators on " + symbol
		print "date: " + x
		print "current price: {5}\n SMA 10: {0}\n SMA 20: {1}\n SMA 50: {2}\n SMA 100: {3}\n SMA 200: {4}".format(sma_10, sma_20, sma_50, sma_100, sma_200, current_price)
	return [current_price, sma_10, sma_20, sma_50, sma_100, sma_200]

def cal_technical_indicators_symbol_list(symbol_source, date):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	data = []
	for symbol in symbol_list:
		r = cal_technical_indicators_symbol(symbol, date)
		row = [symbol] + r
		data.append(row)
	df = pd.DataFrame(data, columns = ['Symbol', 'Current_Price', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_100', 'SMA_200'])
	df.to_csv("data/matrix/mat_price_{0}.csv".format(symbol_source), sep = '\t', index = None)

def cal_integral_ewma_symbol_list(symbol_source, date):
	## symbol_source: tech, health, watch, hold
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		cal_integral_ewma_symbol(symbol, date)

def cal_integral_ewma_symbol(symbol, date):
	fn = 'data/price/{0}/{1}.csv'.format(date, symbol)
	if not os.path.exists(fn):
		print "price file not exists"
		return
	data = pd.read_csv(fn)
	price = data['Close']
	ts = price[::-1]
	ewma_10 = pd.ewma(ts, span = 10, adjust = False)
	ewma_20 = pd.ewma(ts, span = 20, adjust = False)
	
	# print (ewma_10 - ewma_20)[-10:-1]
	integral_10 = sum((ewma_10 - ewma_20)[-10:-5])
	integral_5 = sum((ewma_10 - ewma_20)[-5:-1])
	if integral_10 == 0:
		integral_10 = 0.01
	ratio = abs(integral_5 / integral_10)
	if integral_10 >= 0 and integral_5 >= 0:
		if integral_5 < integral_10:
			signal = 'upside but going down'
		else:
			signal = 'upside and going up'

	elif integral_10 > 0 and integral_5 < 0:
		signal = 'big bear'
	elif integral_10 < 0 and integral_5 > 0:
		if ratio > 1:
			signal = 'big bull'
		else:
			signal = 'small bull'
	else:
		if integral_5 < integral_10:
			signal = 'downside and going down'
		else:
			signal = 'downside but going up'

	print "{0}\t{1}\t{2}\t{3}\t{4}".format(symbol, integral_10, integral_5, signal, ratio)


def cal_cov(symbol_list, date = None, price_from = 'Close', days_length = 90):
	def __standardize(ts):
		mean = np.mean(ts)
		std = np.std(ts)
		return map(lambda x: (x-mean)/std, ts)

	mat = np.zeros([1,days_length])
	names = []
	if not date:
		date = datetime.strftime(datetime.now(), '%m_%d')
	for symbol in symbol_list:
		fn = "data/price/{0}/{1}.csv".format(date, symbol)
		if not os.path.exists(fn):
			print "price file {0} not exists".format(fn)
			continue
		data = pd.read_csv(fn)
		price = np.array(data[price_from])
		if len(price) < days_length:
			continue
		else:
			names.append(symbol)
		ts = __standardize(price[:days_length])
		mat = np.vstack((mat,ts))
	corr = np.corrcoef(mat[1:,:])
	
	# w, v = np.linalg.eig(corr)
	# print w
	# for i in range(len(w)):
	# 	if abs(w[i]) < 0.5:
	# 		print i
	# 		vec = v[:,i]
	# 		for j in range(len(vec)):
	# 			if abs(vec[j])>0.4:
	# 				print names[j]

	# print corr matrix
	# print corr
	for i in range(len(names)):
		for j in range(i+1,len(names)):
			if corr[i,j] > 0.9:
				print names[i], names[j], corr[i,j]
	return
