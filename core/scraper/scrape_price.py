import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame, read_csv
import glob
import time
import numpy as np
import os.path
import urllib
from datetime import datetime


def scrape_price_symbol(symbol):
	# download price data till today
	print "---------- scraping price "+ symbol
	date = datetime.now().strftime("%m_%d")
	path_ = 'data/price/{0}'.format(date)
	if not os.path.exists(path_):
		os.mkdir(path_)
	fn = '{0}/{1}.csv'.format(path_, symbol)
	
	if os.path.exists(fn):
		print "file exists"
		return

	urlHead = 'https://www.google.com/'
	soup = BeautifulSoup(requests.get(urlHead+'finance?q='+symbol).content, 'lxml')
	target = soup.find_all('li', attrs={'class': 'fjfe-nav-sub'})
	# print len(target)
	for item in target:
		if item.text == 'Historical prices':
			tmp2 = item.find('a').get('href')
			soup2 = BeautifulSoup(requests.get(urlHead+tmp2).content, 'lxml')
			try:
				target2 = soup2.find('a', attrs={'class':'nowrap'})
				download_url = target2.get('href')
				testfile = urllib.URLopener()
				testfile.retrieve(download_url, fn)
				print "successfully saved to " + fn
				return
			except:
				print "error: download failed"
	
	print "error: no historical data available"

def scrape_price_symbol_list(symbol_source):
	## symbol_source: tech, health
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		scrape_price_symbol(symbol)


if __name__ == '__main__':

	date = '05_26'
	scrape_price_symbol('HTGM')
	# scrape_price_symbol_list('watch')
	# scrape_price_symbol_list('hold')
	# scrape_price_symbol_list('tech')
	
	# cal_technical_indicators_symbol_list('watch', date)
	# cal_technical_indicators_symbol('NTES', date, silent = False)

	# cal_integral_ewma_symbol_list('watch', date)
	# cal_integral_ewma_symbol_list('tech', date)
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format('semi'))['Symbol']
	# cal_cov(symbol_list, date)
	# cal_cov(['ADI','AAPL'], date)

