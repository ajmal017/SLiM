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


def scrape_supplier_symbol(symbol):
	url = "http://csimarket.com/stocks/competitionNO3.php?supply&code={0}".format(symbol)
	soup = BeautifulSoup(requests.get(url).content, 'lxml')
	# print content
	table = soup.find_all('table')[7]
	# print table
	for tr in table.find_all('tr')[2:-1]:
		print tr.find_all('td')[2].text


if __name__ == '__main__':
	scrape_supplier_symbol('aapl')