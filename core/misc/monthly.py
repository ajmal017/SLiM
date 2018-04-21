import pandas as pd 
import numpy as np 
import matplotlib.pylab as plt
from datetime import datetime
import glob

def monthly_history(mydict, symbol = None, filename = None):
	if symbol:
		filename = "data/price/history/{0}.csv".format(symbol)

	df = pd.read_csv(filename)
	
	df['Y'] = map(lambda x: x.split('-')[0], list(df['Date']))
	df['M'] = map(lambda x: x.split('-')[1], list(df['Date']))
	
	df2 = df[['Y','M','Close']].groupby(['Y','M']).mean()
	# df3 = df[['M',"Close"]].groupby(['M']).mean()
	# df2['YM'] = map(lambda x: datetime.strptime(str(x[0][0])+str(x[0][1])+'01', "%Y%m%d"), df2.iterrows())
	
	for ind, row in df2.iterrows():
		y,m = ind
		price = round(row['Close'],2)
		if y in mydict.keys():
			if m in mydict[y].keys():
				mydict[y][m].append(price)
			else:
				mydict[y][m] = [price]
		else:
			mydict[y] = {}
			mydict[y][m] = [price]

	# df2.to_csv('tmp_AAPL.csv', index = None)
	# plt.plot(df3.index,df3['Close'])
	# plt.plot(dat, df2['Close'])
	# plt.show()

def monthly_one_year(mydict, symbol = None, filename = None):
	if symbol:
		filename = "data/price/06_30/{0}.csv".format(symbol)
	df = pd.read_csv(filename)
	# df['Y'] = map(lambda x: x.split('-')[2], list(df.iloc[:,0]))
	df['M'] = map(lambda x: x.split('-')[1], list(df.iloc[:,0]))
	df3 = df[['M',"Close"]].groupby(['M']).mean()
	
	for ind, row in df3.iterrows():
		price = round(row['Close'],2)
		if ind not in mydict.keys():
			mydict[ind] = [price]
		else:
			mydict[ind].append(price)
	# print mydict

def monthly_one_year_all():
	mydict = {}
	fs = glob.glob('data/price/06_30/*.csv')
	for fn in fs:
		try:
			monthly_one_year(mydict, filename= fn)
		except:
			pass
	for k in mydict.keys():
		mydict[k] = np.mean(mydict[k])
	print mydict

def monthly_history_all():
	mydict = {}
	fs = glob.glob('data/price/history/*.csv')
	for fn in fs:
		try:
			monthly_history(mydict, filename= fn)
		except:
			pass

	for y in mydict:
		print '------- {0} -------'.format(y)
		mydict_sub = mydict[y]
		for k in mydict_sub.keys():
			print k, np.mean(mydict_sub[k]), len(mydict_sub[k])

# monthly_one_year_all()
# monthly_history_all()
mydict = {}
monthly_history(mydict, symbol = 'GSPC')
print mydict