import pandas as pd 
import numpy as np 
import matplotlib.pylab as plt
from datetime import datetime

data = pd.read_csv('../price/CGIX_04_07.csv')
price = np.array(data['Close'])
ts = price[::-1]
date = np.array(data.iloc[:,0])[::-1]
ewma_10 = pd.ewma(ts, span = 10, adjust = False)
ewma_20 = pd.ewma(ts, span = 20, adjust = False)
diff = ewma_10 - ewma_20

up_5d = []
up_10d = []
signal = []
ratio = []
signal_dict = {'big bull': 1, 'small bull': 2, 'upside and going up':3, 'upside but going down': 4, 'downside and going down': 5, 'downside but going up':6, 'bear': 7}

for i in range(9, len(ts) - 10):
	up_5d.append( (ts[i+5] - ts[i]) / ts[i] )
	up_10d.append( (ts[i+10] - ts[i]) / ts[i] )
	int_prev = sum(diff[i-9:i-4])
	int_curr = sum(diff[i-4:i+1])
	if int_prev == 0:
		int_prev = 0.01

	# r = round(abs((int_curr - int_prev) / int_prev), 2)
	r = round(abs(int_curr / int_prev), 2)

	if int_prev >= 0 and int_curr >= 0:
		if int_curr <= int_prev:
			signal.append(signal_dict['upside but going down']) ## ratio < 1
		else:
			signal.append(signal_dict['upside and going up']) ## ratio > 1
		ratio.append(r)
	
	elif int_prev > 0 and int_curr < 0:
		signal.append(signal_dict['bear'])
		ratio.append(0)

	elif int_prev < 0 and int_curr > 0:
		if r > 1:
			signal.append(signal_dict['big bull'])
		else:
			signal.append(signal_dict['small bull'])
		ratio.append(r)
	
	else:
		if int_curr < int_prev:
			signal.append(signal_dict['downside and going down'])
		else:
			signal.append(signal_dict['downside but going up'])
		ratio.append(0)
	

up_5d = map(lambda x: round(x, 2), up_5d)
up_10d = map(lambda x: round(x, 2), up_10d)

with open('signal.txt', 'w') as f:
	for i in range(len(ratio)):
		f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(date[i+9], ts[i+9], signal[i], ratio[i], up_5d[i], up_10d[i]))

ind = range(len(signal))

d = map(lambda x: datetime.strptime(x, "%d-%b-%y"), date)[9: len(ratio) + 9]

# plt.plot(ind, up_5d)
# plt.plot(ind, up_10d)
plt.plot(d, signal, 'o')
plt.plot(d, ts[9: len(ratio) + 9])
x1,x2,y1,y2 = plt.axis()
plt.axis((x1, x2, -1, 10))
plt.show()

def get_ewma_ts(symbol, price):
	pass
	
def X(rel_ewma_ts, delta_t_back):
	# rel_ewma_ts : (ewma_5 - ewma_10) / ewma_10 or (ewma_10 - ewma_20) / ewma_20
	# price: Close, Open, High, Low
	# return: sum(rel_ewma_ts(x-i)) for i = 0,1,2...delta_t_back
	pass

def Y(price_ts, delta_t_ahead):
	# price: Close, Open, High, Low
	# return: (y(x+delta_t_ahead) - y(x)) / y(x)
	pass

