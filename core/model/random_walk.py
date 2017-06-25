import pandas as pd
import random
import os.path
import numpy as np 

def random_walk(k = 300):
	symbol_list = pd.read_csv('data/symbol/tech.csv')['Symbol']
	# print len(symbol_list)
	symbol_sample = random.sample(symbol_list, k)
	roe_list = []
	neg = 0
	for symbol in symbol_sample:
		fn = 'data/price/05_26/{}.csv'.format(symbol)
		if os.path.exists(fn):
			price = list(pd.read_csv(fn)['Close'])
			if len(price)>100:
				# prev = price[-len(price)/2]
				prev = price[-1]
				after = price[0]
				if prev > after:
					neg += 1
				roe = (after - prev)*1.0/prev
				roe_list.append(roe)
				# print symbol, roe
	print "[sample num: {0}] average: {1}, deviation: {2}".format(len(roe_list), round(np.mean(roe_list), 2), round(np.std(roe_list), 2))
	print "negative return: ", neg
if __name__ == '__main__':
	random_walk(k = 100)
	random_walk(k = 200)
	random_walk(k = 300)