import pandas as pd 
import numpy as np 
import glob

def search_top(loc):
	fs = glob.glob(loc)
	with open('research.txt','w') as f:
		f.write('Symbol,prev,curr,rate(%)\n')
		for fn in fs:
			data = pd.read_csv(fn)
			price = np.array(data['Close'])
			if len(price) <= 0:
				continue
			up = round((price[0] - price[-1])/price[-1],2) *100
			if up>100:
				f.write('{0},{1},{2},{3}\n'.format(fn.split('/')[-1].split('_')[0], price[-1], price[0], up))


def search_golden_cross(symbol):
	fn = 'price/04_20/AMD.csv'
	data = pd.read_csv(fn)
	price = np.array(data['Close'])[::-1]
	# date = map(lambda x: datetime.strptime(x, "%d-%b-%y"), list(data.iloc[:,0])[::-1])
	date = list(data.iloc[:,0])[::-1]
	ewma_10 = pd.ewma(price, span = 10, adjust = False)
	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	ewma_50 = pd.ewma(price, span = 50, adjust = False)
	ewma_200 = pd.ewma(price, span = 200, adjust = False)
	



# search_top(loc = 'price/04_06/*.csv')