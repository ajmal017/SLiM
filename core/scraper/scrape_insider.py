import requests
import urllib
import pandas as pd
from pandas import DataFrame, read_csv
import glob
import logging
import random
import numpy as np
import os.path
from bs4 import BeautifulSoup
from lxml import html  
from exceptions import ValueError
from time import sleep
import json
# import argparse
from collections import OrderedDict
from time import sleep
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')



# urlHead = 'http://www.insider-monitor.com/reports/insider-buys-20170322.html'
def scrape_insider_weekly(week_from = '0320'):
	
	data = {}
	l = []
	urlHead = 'http://www.insider-monitor.com/top10_insider_buys_week.html'
	soup = BeautifulSoup(requests.get(urlHead).content, 'lxml')
	table = soup.find_all('table')[0]
	trs = table.find_all('tr')
	
	title = soup.find('title').text
	page_num = int(title.split(' ')[-1].replace(')', ''))
	i = 2
	while i <= page_num:
		url_ = 'http://www.insider-monitor.com/top10_insider_buys_week-{0}.html'.format(i)
		soup_ = BeautifulSoup(requests.get(url_).content, 'lxml')
		trs_ = table.find_all('tr')
		trs += trs_
		i += 1

	for tr in trs:
		tds = tr.find_all('td')
		if len(tds) == 7:
			if tds[1].text != '':
				symbol = tds[0].text
				shares = locale.atof(tds[3].text)
				# price = tds[4].text
			else:
				shares = locale.atof(tds[3].text)
			l.append(symbol)
			if symbol not in data.keys():
				data[symbol] = shares
			else:
				data[symbol] += shares

	for k in data.keys():
		if data[k] < 10000 or data[k]> 100000:
			data[k] = 0
		else:
			data[k] = 1
	data = pd.DataFrame(data.items(), columns = ['Symbol', 'Shares Signal'])
	data.to_csv('symbol/INSIDER_{0}.csv'.format(week_from), index = None)


if __name__ == '__main__':
	scrape_insider_weekly(week_from = '0320')


