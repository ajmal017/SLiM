import pandas as pd 
from datetime import datetime
import numpy as np 
import matplotlib.pylab as plt 
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,6
# import statsmodels
from statsmodels.tsa.stattools import adfuller
# print statsmodels.__file__
# from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

def date_clean(x):
	x_time = datetime.strptime(x, '%m/%d/%Y')

	return x_time.strftime('%Y-%m-%d')

def clean(stockname = "AMD"):
	data = pd.read_csv(stockname +".csv")
	data = data.iloc[::-1]
	# data = data.reindex(index=data.index[::-1])
	date = data['Date']
	date_2 = map(lambda x: date_clean(x), date)
	data['Date'] = date_2
	data.to_csv("AMD.csv", index = None)

def plt_moving_avg(stockname, itemname, timeseries):
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=30)
    rolstd = pd.rolling_std(timeseries, window=30)

    #Plot rolling statistics:
    plt.clf()
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation on {0} {1}'.format(stockname,itemname))
    plt.savefig('{0}_{1}.png'.format(stockname,itemname))
    return 
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput

def plt_seasonal(stockname, itemname, ts):
	decomposition = seasonal_decompose(ts)

	trend = decomposition.trend
	seasonal = decomposition.seasonal
	residual = decomposition.resid
	plt.clf()
	plt.subplot(411)
	plt.plot(ts_log, label='Original')
	plt.legend(loc='best')
	plt.subplot(412)
	plt.plot(trend, label='Trend')
	plt.legend(loc='best')
	plt.subplot(413)
	plt.plot(seasonal,label='Seasonality')
	plt.legend(loc='best')
	plt.subplot(414)
	plt.plot(residual, label='Residuals')
	plt.legend(loc='best')
	plt.tight_layout()
	plt.title('Seasonal Decomposition on {0} {1}'.format(stockname,itemname))
	plt.savefig('{0}_{1}_seasonal.png'.format(stockname,itemname))

def plt_acf(ts):
	ts_diff = (ts - ts.shift())[1:]
	print ts_diff
	lag_acf = acf(ts_diff, nlags=20)
	lag_pacf = pacf(ts_diff, nlags=20, method='ols')
	#Plot ACF: 
	plt.subplot(121) 
	plt.plot(lag_acf)
	plt.axhline(y=0,linestyle='--',color='gray')
	plt.axhline(y=-1.96/np.sqrt(len(ts_diff)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(ts_diff)),linestyle='--',color='gray')
	plt.title('Autocorrelation Function')
	#Plot PACF:
	plt.subplot(122)
	plt.plot(lag_pacf)
	plt.axhline(y=0,linestyle='--',color='gray')
	plt.axhline(y=-1.96/np.sqrt(len(ts_diff)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(ts_diff)),linestyle='--',color='gray')
	plt.title('Partial Autocorrelation Function')
	plt.tight_layout()
	plt.show()

def ARIMA_model(stockname, itemname, ts):
	ts_diff = (ts - ts.shift(2))[2:]
	
	## AR model
	plt.clf()
	model_1 = ARIMA(ts.as_matrix(), order=(3, 2, 0))  
	results_AR = model_1.fit(disp=-1)  
	plt.plot(ts_diff)
	plt.plot(results_AR.fittedvalues, color='red')
	plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_diff)**2))
	plt.savefig('{0}_{1}_AR.png'.format(stockname, itemname))
	
	# MA model
	plt.clf()
	model_2 = ARIMA(ts.as_matrix(), order=(0, 2, 2))  
	results_MA = model_2.fit(disp=-1)  
	plt.plot(ts_diff)
	plt.plot(results_MA.fittedvalues, color='red')
	plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_diff)**2))
	plt.savefig('{0}_{1}_MA.png'.format(stockname, itemname))

	# ARIMA model
	plt.clf()
	model = ARIMA(ts.as_matrix(), order=(3, 2, 2))  
	results_ARIMA = model.fit(disp=-1)  
	plt.plot(ts_diff)
	plt.plot(results_ARIMA.fittedvalues, color='red')
	plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_diff)**2))
	plt.savefig('{0}_{1}_ARIMA.png'.format(stockname, itemname))

if __name__ == '__main__':
	data = pd.read_csv("AMD.csv", index_col = 'Date')
	# plt_moving_avg('AMD', 'Open', data['Open'])
	# plt_moving_avg('AMD', 'Close', data['Close'])
	# plt_moving_avg('AMD', 'Volume', data['Volume'])
	# print data['Open']
	# plt_acf(data['Open'])
	ts = data['Open']
	# ARIMA_model('AMD', 'Open', ts)