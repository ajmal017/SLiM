# -*- coding: utf-8 -*-
import csv
import requests
import urllib
import pandas as pd
import glob
import logging
import random
import numpy as np
import os.path
from bs4 import BeautifulSoup
from lxml import html  
# from exceptions import ValueError
from time import sleep
import json
from collections import OrderedDict
from time import sleep
import os
from datetime import datetime, timedelta
# https://query2.finance.yahoo.com/v10/finance/quoteSummary/aapl?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com

def scrape_report_weekly(p1, p2):
	# example p1, p2 format '2017-04-02'
	d1 = datetime.strptime(p1, '%Y-%m-%d')
	d2 = datetime.strptime(p2, '%Y-%m-%d')
	date = d1 + timedelta(days = 1)
	while date < d2:
		date_str = datetime.strftime(date, '%Y-%m-%d')
		yahoo_url = 'https://finance.yahoo.com/calendar/earnings?from={0}&to={1}&day={2}&sf=epssurprisepct&st=desc'.format(p1,p2,date_str)
		# yahoo_url = 'https://finance.yahoo.com/calendar/earnings?from={0}&to={1}&day={2}'.format(p1,p2,date_str)
		soup = BeautifulSoup(requests.get(yahoo_url).content, 'lxml')
		# print yahoo_url
		tables = soup.find_all("table")
		# print len(tables)
		# return
		trs = tables[0].find_all("tr")
		df = []
		for tr in trs[1:]:
			try:
				symbol = tr.find("a").text
				if len(symbol.split('.')) > 1:
					continue
				td = tr.find_all('td')
				pubTime = td[2].text
				est = td[3].text
				act = td[4].text
				df.append([symbol, pubTime, est, act])
			except:
				pass
		if len(df) != 0:
			data = pd.DataFrame(df, columns = ['Symbol', 'pubTime', 'estimate', 'actual'])
			data.to_csv('data/eps/report_{0}.csv'.format(date_str), index = None)
		date += timedelta(days = 1)


def scrape_report_symbol(symbol):
	print("===============================")
	print("scraping report on {}".format(symbol))
	yahoo_url = 'https://finance.yahoo.com/calendar/earnings?symbol={0}'.format(symbol)
	soup = BeautifulSoup(requests.get(yahoo_url).content, 'lxml')
	# print yahoo_url
	try:
		tables = soup.find_all("table")
		trs = tables[1].find_all("tr")
		for tr in trs:
			tds = tr.find_all('td')
			for td in tds:
				print(td.text)
	except:
		print('Scraping failed')
		pass


def scrape_report_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		scrape_report_symbol(symbol)


def scrape_finanace_summary_list(symbol_source):
	## symbol_source: tech, health
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		sleep(2)
		scrape_finance_summary_symbol(symbol, symbol_source)


def scrape_finance_summary_symbol(symbol, sector = None):
	print("Parsing {}".format(symbol))
	sleep(2)

	############ parsing summary ##########
	url = "https://finance.yahoo.com/quote/%s?p=%s"%(symbol,symbol)
	response = requests.get(url)
	parser = html.fromstring(response.text)
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
	summary_data = OrderedDict()
	for table_data in summary_table:
		raw_table_key = table_data.xpath('.//td[@class="C(black)"]//text()')
		raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
		table_key = ''.join(raw_table_key).strip()
		table_value = ''.join(raw_table_value).strip()
		summary_data.update({table_key:table_value})

	if sector:
		fn = 'data/json/{0}/summary_{1}.json'.format(sector, symbol)
	else:
		fn = 'data/json/summary_{0}.json'.format(symbol)
	with open(fn,'w') as fp:
		json.dump(summary_data, fp, indent = 4)
 
def scrape_finance_all_list(symbol_source):
	## symbol_source: tech, health
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	for symbol in symbol_list:
		scrape_finance_all_symbol(symbol, symbol_source)

def scrape_finance_all_symbol(symbol, sector = None):
	print("Scraping finance data on {}".format(symbol))
	
	if sector:
		fn = 'data/json/{0}/all_{1}.json'.format(sector, symbol)
	else:
		fn = 'data/json/all_{0}.json'.format(symbol)
	if os.path.exists(fn):
		print("file exists")
		return
	########### parsing all details ########
	json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(symbol)
	json_response = requests.get(json_link)
	json_loaded =  json.loads(json_response.text)

	with open(fn,'w') as f:
		json.dump(json_loaded, f, indent = 4)


if __name__=='__main__':
	
	# scrape_finance_summary_symbol('AMD')
	# scrape_finance_all_symbol('AMD')

	# scrape_finanace_summary_list('tech')
	scrape_finance_all_list('watch')
