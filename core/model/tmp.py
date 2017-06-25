import pandas as pd 
import numpy as np 
import glob

def make_matrix_perf(filename, delta_past_t = 5, delta_future_t = 10, thre = 0.05):
	data = pd.read_csv(filename)
	price = np.array(data['Close'])[::-1]
	# date = np.array(data.iloc[:,0])[::-1]
	
	ewma_5 = pd.ewma(price, span = 5, adjust = False)
	ewma_10 = pd.ewma(price, span = 10, adjust = False)
	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	ts_510 = (ewma_5 - ewma_10) / ewma_10
	ts_1020 = (ewma_10 - ewma_20) / ewma_20

	row = []
	for i in range(delta_past_t, len(price) - delta_future_t):
		X1 = list(ts_510[(i - delta_past_t) : i])
		X2 = list(ts_1020[(i - delta_past_t) : i])
		X = X1 + X2
		Y = (price[i + delta_future_t] - price[i])/price[i]
		if Y > thre:
			row.append(X + [1])
		else:
			row.append(X + [0])
	# row2 = map(lambda x: 1 if x[10] > 0.1 else 0, row)
	df = pd.DataFrame(row)
	return df

fs = glob.glob('../price/04_06/*.csv')
frame = []
for i in range(len(fs)):
	fn = fs[i]
	df = make_matrix_perf(fn)
	frame.append(df)

DF = pd.concat(frame)
print DF.shape
print(sum(DF.iloc[:,10]>0))


