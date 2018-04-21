import urllib
import json
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd 
import glob
from datetime import datetime, timedelta
import time
import os


def scrape_rss_symbol(symbol, rss_date):
	# rss_cate: watch, hold, report, x
	path_ = 'data/rss/{0}'.format(rss_date)
	if not os.path.exists(path_):
		os.mkdir(path_)
		
	# if not rss_date:
	# 	rss_date = datetime.strftime(datetime.now(), '%m%d')
	
	fn = 'data/rss/{0}/{1}.csv'.format(rss_date, symbol)
	if os.path.exists(fn):
		print("file exists")
		return
	
	print('scraping rss on {0}'.format(symbol))
	
	root = ET.fromstring(requests.get("http://finance.yahoo.com/rss/headline?s={0}".format(symbol)).content)
	rss_list = []
	for child in root[0]:
		if child.tag == 'item':
			row = ['','','']
			for subChild in child:
				if subChild.tag == 'title':
					row[0] = subChild.text.encode('utf-8')
				if subChild.tag == 'pubDate':
					row[1] = subChild.text.encode('utf-8')
				if subChild.tag == 'link':
					row[2] = subChild.text.encode('utf-8')
			rss_list.append(row)

	col = ['title', 'pubDate', 'link']
	rss_data = pd.DataFrame(rss_list, columns = col)
	rss_data = rss_data.drop_duplicates(['title'])
	rss_data.to_csv(fn, sep = ',', index = None)


def scrape_rss_list(source_from, rss_date):

	symbol_list = pd.read_csv("data/symbol/{0}.csv".format(source_from))['Symbol']
	for symbol in symbol_list:
		scrape_rss_symbol(symbol, rss_date)


def push_rss_html(source_from, rss_date, since_date, report = False):

	l = []
	symbol_list = pd.read_csv("data/symbol/{0}.csv".format(source_from))['Symbol']
	
	since = datetime.strptime(since_date, "%y%m%d")

	for symbol in symbol_list:
		fn = 'data/rss/{0}/{1}.csv'.format(rss_date, symbol)
		d = pd.read_csv(fn)
		l.append([symbol])
		for ind, row in d.iterrows():
			utc = datetime.strptime(row['pubDate'], '%a, %d %b %Y %H:%M:%S +0000')
			local = utc - timedelta(hours = 7)
			local_str = local.strftime("%a, %d %b %Y %H:%M:%S")
			diff = (local - since).days
			local_short = local.strftime("%m%d")
			if diff >= 0:
				l.append([row['title'], local_str, row['link']])
	if not report:
		text = ""
		text += '<!DOCTYPE html>\n'
		text += '<html><head><title>{0}</title></head><body>\n'.format("title")
		for item in l:
			if len(item) == 1:
				text += '<div><p>------ {0} ------</p></div>'.format(item[0])
			else:
				link = item[2]
				date = item[1]
				title = item[0]
				text += '<div><a href = \'{0}\'>{1}</a><p>publish date (local time/PST): {2}</p></div>'.format(link, title, date)
			text += '</body></html>'
		return text

	else:
		fn_out = 'report/news_{0}_{1}.html'.format(source_from, rss_date)
			
		if os.path.exists(fn_out):
			os.remove(fn_out)

		with open(fn_out, 'w') as f:
			f.write('<!DOCTYPE html>\n')
			f.write('<html><head><title>{0}</title></head><body>\n'.format(fn_out))
			for item in l:
				if len(item) == 1:
					f.write('<div><p>------ {0} ------</p></div>'.format(item[0]))
				else:
					link = item[2]
					date = item[1]
					title = item[0]
					f.write('<div><a href = \'{0}\'>{1}</a><p>publish date (local time/PST): {2}</p></div>'.format(link, title, date))
			f.write('</body></html>')
		print('pushing news from {0} to {1}'.format(rss_date, fn_out))


if __name__ == '__main__':
	pass
	# scrape_rss_symbol('^IXIC', 'x')
	# push_rss_html('x', news_date = ['0325', '0326', '0327', '0328'])

	# scrape_rss_list(source_from = 'hold', rss_cate = 'hold')
	# scrape_rss_list(source_from = 'watch', rss_cate = 'watch')
	# push_rss_html(rss_cate = 'watch', news_date = ['0325', '0326', '0327', '0328'])
	# push_rss_html(rss_cate = 'hold', news_date = None)


