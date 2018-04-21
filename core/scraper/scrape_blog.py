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


def scrape_blog(sector, content = False, page = 3):
	row = []
	header = 'https://seekingalpha.com'

	for p in range(1, page+1):
		print "scaping page {}".format(p)
		url = 'https://seekingalpha.com/stock-ideas/{0}?page={1}'.format(sector, p)
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		# u'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
		# u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
		response = requests.get(url, headers = headers)
		print response.status_code
		parser = html.fromstring(response.text)
		data_div = parser.xpath('//li[contains(@class,"article media")]//div[contains(@class, "media-body")]')
		
		for div in data_div:
			span = div.xpath('.//span//text()')			
			date = span[2].encode('utf-8').strip()
			symbol = div.xpath('.//a//text()')[1]
			title = div.xpath('.//a[contains(@class, "a-title")]//text()')[0].encode('utf-8').strip()
			url = div.xpath('.//a[contains(@class, "a-title")]//@href')[0]
			# print symbol, title, url
			url = str(header)+str(url)
			if content:
				scrape_content(url, symbol)
			row.append([symbol, title, url, date])
	
	df = pd.DataFrame(row, columns = ['Symbol', 'Title', 'URL', 'Date'])
	today = datetime.today().strftime('%m-%d')
	# print df.head(4)
	df.to_csv("data/blog/{0}_{1}.csv".format(sector, today), index = None)


def push_blog_html(sector):
	today = datetime.today().strftime('%m-%d')

	file_out = 'report/blog_{0}_{1}.html'.format(sector, today)	
	if os.path.exists(file_out):
		os.remove(file_out)

	file_in = 'data/blog/{0}_{1}.csv'.format(sector, today)
	d = pd.read_csv(file_in)
		
	with open(file_out, 'w') as f:
		f.write('<!DOCTYPE html>\n')
		f.write('<html><head><title>blog of {}</title></head><body>\n'.format(sector))
		for ind, row in d.iterrows():
			symbol = row['Symbol']
			date = row['Date']
			url = row['URL']
			title = row['Title']
			f.write('<div><a href = \'{0}\'>{3}: {1}</a><p>publish date (local time/PST): {2}</p></div>'.format(url, title, date, symbol))
		f.write('</body></html>')

	print('pushing blog of {}'.format(sector))

def scrape_content(url, symbol):
	# url = 'https://seekingalpha.com/article/4108932-amd-nvidia-still-undervalued'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	response = requests.get(url, headers = headers)
	print response.status_code
	parser = html.fromstring(response.text)
	summary = parser.xpath('//div[contains(@class, "a-sum")]//text()')
	text = parser.xpath('//p//text()')
	# print summary

	with open('text_output/{0}_blog.txt'.format(symbol), 'w') as f:
		for s in summary:
			f.write(s.encode('utf-8').strip())
		for t in text:
			if len(t) > 5:
				f.write(t.encode('utf-8').strip())
	

if __name__ == '__main__':
	# scrape_blog(sector = 'technology', content = True, page = 3)
	# push_blog_html(sector = 'technology')
	url = 'https://seekingalpha.com/article/4162116-pure-storage-company-stay'
	scrape_content(url, symbol = 'PSTG')