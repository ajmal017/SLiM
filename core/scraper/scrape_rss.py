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

def scrape_rss_symbol(symbol, rss_cate = 'x', rss_date = None):
	# rss_cate: watch, hold, report, x
	path_ = 'data/rss/{0}'.format(rss_cate)
	if not os.path.exists(path_):
		os.mkdir(path_)
		
	if not rss_date:
		rss_date = datetime.strftime(datetime.now(), '%m%d')
	fs = glob.glob('data/rss/{0}/rss_{1}_*.csv'.format(rss_cate, symbol))
	for f in fs:
		os.remove(f)
	print 'scraping rss on {0}'.format(symbol)
	root = ET.fromstring(requests.get("http://finance.yahoo.com/rss/headline?s={0}".format(symbol)).content)
	rss_list = []
	for child in root[0]:
		if child.tag =='item':
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
	rss_data.to_csv('data/rss/{0}/rss_{1}_{2}.csv'.format(rss_cate, symbol, rss_date), sep = ',', index = None)

def scrape_rss_list(source_from, rss_cate):
	# source_from: hold, REPORT_*, INSIDER_*, 
	# rss_cate: watch, hold, x
	if rss_cate == 'report':
		date = source_from.split('_')[-1]
		rss_cate = '/'.join([rss_cate, date])

	symbol_list = pd.read_csv("data/symbol/{0}.csv".format(source_from))['Symbol']
	for symbol in symbol_list:
		scrape_rss_symbol(symbol, rss_cate)

# def push_rss(rss_cate, news_date, simple = False):
# 	# rss_cate: watch, hold, report, x

# 	files = glob.glob('rss/' + rss_cate + '/*.csv')
# 	l = []
# 	for f in files:
# 		d = pd.read_csv(f)
# 		l.append("====== " + f.split('.')[0] + " =======\n")
# 		for ind, row in d.iterrows():
# 			prev = datetime.strptime(row['pubDate'], '%a, %d %b %Y %H:%M:%S GMT')
# 			after = prev.strftime("%m%d")
# 			if after in news_date:
# 				l.append(row['title'])
# 				if not simple:
# 					l.append('\t'.join([row['pubDate'], row['link']]))
# 					l.append('\n')
# 		l.append('================================')
	
# 	fn = 'news/news_{0}_{1}_{2}.txt'.format(rss_cate, news_date[0], news_date[-1]) 
	
# 	if os.path.exists(fn):
# 		os.remove(fn)

# 	with open(fn, 'a+') as f:
# 		for item in l:
# 			f.write(item)
# 			f.write('\n')

def push_rss_html(rss_cate, news_date):
	# rss_cate: watch, hold, report, x

	files = glob.glob('data/rss/' + rss_cate + '/*.csv')
	l = []
	for f in files:
		d = pd.read_csv(f)
		symbol = f.split('.')[0].split('/')[-1].split('_')[1]
		l.append([symbol])
		for ind, row in d.iterrows():
			utc = datetime.strptime(row['pubDate'], '%a, %d %b %Y %H:%M:%S +0000')
			local = utc - timedelta(hours = 7)
			local_str = local.strftime("%a, %d %b %Y %H:%M:%S")
			local_short = local.strftime("%m%d")
			if not news_date or local_short in news_date:
				l.append([row['title'], local_str, row['link']])
	
	if news_date:
		fn = 'report/news_{0}_{1}_{2}.html'.format(rss_cate, news_date[0], news_date[-1]) 
	else:
		fn = 'report/news_{0}_today.html'.format(rss_cate)
		
	if os.path.exists(fn):
		os.remove(fn)

	with open(fn, 'w') as f:
		f.write('<!DOCTYPE html>\n')
		f.write('<html><head><title>{0}</title></head><body>\n'.format(fn))
		for item in l:
			if len(item) == 1:
				f.write('<div><p>------ {0} ------</p></div>'.format(item[0]))
			else:
				link = item[2]
				date = item[1]
				title = item[0]
				f.write('<div><a href = \'{0}\'>{1}</a><p>publish date (local time/PST): {2}</p></div>'.format(link, title, date))
		f.write('</body></html>')
	print('pushing news from {0} to {1}'.format(rss_cate, fn))

if __name__ == '__main__':
	pass
	# scrape_rss_symbol('^IXIC', 'x')
	# push_rss_html('x', news_date = ['0325', '0326', '0327', '0328'])

	# scrape_rss_list(source_from = 'hold', rss_cate = 'hold')
	# scrape_rss_list(source_from = 'watch', rss_cate = 'watch')
	# push_rss_html(rss_cate = 'watch', news_date = ['0325', '0326', '0327', '0328'])
	# push_rss_html(rss_cate = 'hold', news_date = None)


