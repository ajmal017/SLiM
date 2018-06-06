import requests
import urllib
import pandas as pd
import numpy as np
import os.path
from bs4 import BeautifulSoup
from lxml import html  
import json
import os
from datetime import datetime, timedelta


def scrape_holdings(symbol):
	page = 1
	df = []
	fil = "data/symbol/etf/{}_holdings.csv".format(symbol)
	# if os.path.exists(fil):
	# 	print("file exists")
	# 	return
		
	while page < 2:
		url = 'http://etfdb.com/etf/{0}/#etf-holdings&sort_name=weight&sort_order=desc&page={1}'.format(symbol, page)
		print(url)
		page += 1
		soup = BeautifulSoup(requests.get(url).content, 'lxml')
		tables = soup.find_all("table")
		trs = tables[3].find_all("tr")
		
		for tr in trs[1:-1]:
			tds = tr.find_all('td')
			s = tds[0].text.split(' ')[-1].replace("(", "").replace(")", "")
			weight = tds[1].text
			df.append([s, weight])
	
	df = pd.DataFrame(df, columns = ['Symbol', 'Weight'])
	
	df.to_csv(fil, index = None)

def scrape_holdings_list(symbol_source):
	symbol_list = pd.read_csv("data/symbol/{}.csv".format(symbol_source))['Symbol']
	for symbol in symbol_list:
		scrape_holdings(symbol)

def analyse_holdings(symbol_source):
	etf = pd.read_csv("data/symbol/{}.csv".format(symbol_source))["Symbol"]
	dict_etf = {}
	for s in etf:
		data = pd.read_csv("data/symbol/etf/{}_holdings.csv".format(s))
		for ind, row in data.iterrows(): 
			symbol = row["Symbol"]
			weight = float(row['Weight'].replace("%", ""))
			if symbol in dict_etf.keys():
				dict_etf[symbol].append(weight)
			else:
				dict_etf[symbol] = [weight]
	for k in dict_etf:
		print(k, dict_etf[k])

if __name__ == '__main__':
	# symbol = 'ARKW'

	# scrape_holdings(symbol)

	# scrape_holdings_list("watch_etf")
	analyse_holdings("watch_etf")

