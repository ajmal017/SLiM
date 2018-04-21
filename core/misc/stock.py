'''
This script is written to scrape historical stock prices from Google Finance
Date: Dec 23, 2015
Author: Jing Ye
'''

import csv
import requests
from BeautifulSoup import BeautifulSoup
import urllib
import pandas as pd
from pandas import DataFrame, read_csv
import glob
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import time
import random
import numpy as np
import os.path

urlHead = 'https://www.google.com/'

def stockPriceScraper(symbol):
	print symbol
	logging.info(symbol)
	filename = './price-tech/'+symbol+".csv"

	if os.path.exists(filename):
		logging.info('file exists')
		print "file exists"
		return
	
	soup = BeautifulSoup(requests.get(urlHead+'finance?q='+symbol).content)
	target = soup.findAll('li', attrs={'class': 'fjfe-nav-sub'})

	for item in target:

		if item.text == 'Historical prices':
			tmp2 = item.find('a').get('href')
			
			soup2 = BeautifulSoup(requests.get(urlHead+tmp2).content)
			try:
				target2 = soup2.find('a', attrs={'class':'nowrap'})
				download_url = target2.get('href')
				testfile = urllib.URLopener()
				testfile.retrieve(download_url, filename)
				logging.info('success')
				print "success"
			except:
				print "fail"
		else:
			print "no historical data"

def dataLoad(symbolList):
	for symbol in symbolList:
		stockPriceScraper(symbol)

def getLabel_1(prices,s1,s2,t):
	while prices[s2] == 0:
		s2 += 1
		s1 -= 1
	flag = (prices[t]-prices[s2])/prices[s2]
	
	if flag >= 0.1:
		label = 1
	elif flag <= -0.1:
		label = -1
	else:
		label = 0
	features = prices[s1:s2+1]

	return label,features

def getLabel_2(prices,s1,s2,t):
	
	flag = prices[t]-prices[s2]
	
	if flag > 0:
		label = 1
	else:
		label = -1
	
	features = prices[s1:s2+1]

	return label,features

def makeDataMatrix(signal,s1,s2,t):
	filenames = glob.glob("./data/*.csv")
	matrix = []
	names = []
	#print len(filenames)
	for fn in filenames:
		DF = read_csv(fn)
		prices = list(DF[signal])
		if len(prices)>t:
			symbol = fn.split('/')[2].split('.')[0]
			names.append(symbol)
			prices = prices[::-1]
			if type(prices[0]!=type(0.1)):
				prices = [float(x) if x!='-' else 0 for x in prices]
			l,f = getLabel_2(prices,s1,s2,t)
			f.append(l)
			matrix.append(f)
	
	return DataFrame(matrix,index = names)

def dataSplit(DATA,train_rate):

	length = DATA.shape[0]
	
	train_index = random.sample(range(length),int(length*train_rate))
	test_index = list(set(range(length))-set(train_index))
	TRAIN = DATA.iloc[train_index,:]
	TEST = DATA.iloc[test_index,:]

	return TRAIN,TEST

def scale(dataframe):
	new_row = []
	for index,row in dataframe.iterrows():	
		new_row.append((row - np.mean(row))/np.std(row))
	
	return DataFrame(new_row)
			


def RFClassifier(parameters,DATA):

	[TRAIN,TEST] = DATA
	num_of_trees = parameters
	
	label_train = TRAIN.iloc[:,-1]
	label_test = TEST.iloc[:,-1]
	
	col_num = TEST.shape[1]
	
	feature_train = scale(TRAIN.iloc[:,:col_num-1])
	feature_test = scale(TEST.iloc[:,:col_num-1])
	

	# n_estimators : number of trees
	RFC = RandomForestClassifier(n_estimators = num_of_trees)

	print "...Random Forest Classifier training, number of trees is :", num_of_trees
	RFC = RFC.fit(feature_train,label_train)


	fit_train = DataFrame(RFC.predict(feature_train))
	fit_test = DataFrame(RFC.predict(feature_test))
	
	conf_train = DataFrame(RFC.predict_proba(feature_train))
	conf_test = DataFrame(RFC.predict_proba(feature_test))

	result_train = pd.concat([TRAIN,fit_train,conf_train],axis=1) 
	result_test = pd.concat([TEST,fit_test,conf_test],axis=1)
	
	result_train.to_csv("rf.result.train.csv",index=None)
	result_test.to_csv("rf.result.test.csv",index=None)

	score_train = RFC.score(feature_train,label_train)
	score_test = RFC.score(feature_test,label_test)
	print "accuracy for train:",score_train
	print "accuracy for test:",score_test
	
	return score_train,score_test

def SVMClassifier(DATA):

	[TRAIN,TEST] = DATA
	
	label_train = TRAIN.iloc[:,-1]
	label_test = TEST.iloc[:,-1]
	
	feature_train = scale(TRAIN.iloc[:,:(s+1)])
	feature_test = scale(TEST.iloc[:,:(s+1)])
	print "...SVM Classifier training"
	SVC = svm.SVC()
	SVC = SVC.fit(feature_train,label_train)
	
	fit_train = DataFrame(SVC.predict(feature_train))
	fit_test = DataFrame(SVC.predict(feature_test))
	
	result_train = pd.concat([TRAIN.reset_index(),fit_train],axis=1) 
	result_test = pd.concat([TEST.reset_index(),fit_test],axis=1)
	result_train.to_csv("svm.result.train.csv",index=None)
	result_test.to_csv("svm.result.test.csv",index=None)

	score_train = SVC.score(feature_train,label_train)
	score_test = SVC.score(feature_test,label_test)
	print "accuracy for train:",score_train
	print "accuracy for test:",score_test
	
	return score_train,score_test



if __name__=="__main__":
	
	logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
	
	symbolList = list(read_csv('symbol/tech-companylist.csv')['Symbol'])

	# dataLoad(symbolList[:])
	stockPriceScraper("SNAP")
	# s1 = 0
	# s2 = 90
	# t = 150
	
	# matrix1 = makeDataMatrix('Open')
	# matrix1.to_csv("matrix/open.csv")

	# matrix2 = makeDataMatrix('Close',s1,s2,t)
	# matrix2.to_csv("matrix/close.csv")
	
	# matrix3 = makeDataMatrix('Low')
	# matrix3.to_csv("matrix/low.csv")

	# matrix4 = makeDataMatrix('High')
	# matrix4.to_csv("matrix/high.csv")

	# print matrix1.shape,matrix2.shape,matrix3.shape,matrix4.shape

	# train,test = dataSplit(matrix2,0.6)
	# RFClassifier(5,[train,test])
	# s = 0

	# for dur in [40,50,60]:
	# 	print "------",dur,'--------'
	# 	matrix = makeDataMatrix('Close',s,s+dur,s+2*dur)
	# 	train,test = dataSplit(matrix,0.6)
	# 	RFClassifier(5,[train,test])
	
	#SVMClassifier([train,test])
