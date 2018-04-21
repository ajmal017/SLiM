import glob
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import os.path

def scrape_gurus(name, this_date):
	print('scrpaing gurus {0} on date {1}'.format(name, this_date))
	row = []
	# order = 'date'
	output_ = 'data/gurus/{0}_{1}.csv'.format(name, this_date)
	if os.path.exists(output_):
		print("file exist")
		return

	for page in range(20):
		print("scraping on page {}".format(page))
		url = 'https://www.gurufocus.com/StockBuy.php?GuruName={0}&cache=clear&action=all&updown=down&order=date&view=list&p={1}&n=100'.format(name, page)
		# print url
		soup = BeautifulSoup(requests.get(url).content, 'lxml')
		tables = soup.find_all("table")
		trs = tables[0].find_all("tr")
		df = []
		for tr in trs[1:]:
			tds = tr.find_all('td')
			if len(tds) == 12:
				ticker = tds[0].text
				date = tds[2].text
				action = tds[3].text
				price = tds[6].text[3:]
				comment = tds[8].text
				shares = tds[9].text.replace(',','')
				if date == this_date:
					row.append([ticker, date, action, comment, shares, price])
		if date < this_date:
			# print "date is finished"
			break
	df = pd.DataFrame(row, columns = ['Symbol', 'Date', 'Action', 'Comment', 'Shares', 'Price'])
	
	df.to_csv(output_, index = None)

def filter_gurus(date, sector = 'tech', extend_list = []):
	symbol_list = list(pd.read_csv('data/symbol/{}.csv'.format(sector))['Symbol'])
	symbol_list += extend_list

	gurus_files = glob.glob("data/gurus/*_{}.csv".format(date))
	new_row_buy = []
	new_row_sell = []
	# print gurus_files
	for fil in gurus_files:
		gurus_name = fil.split("/")[-1].split("_")[0]
		data = pd.read_csv(fil)
		for ind,row in data.iterrows():
			act = row["Action"].replace(" ", "")
			if row["Symbol"] in symbol_list:
				if act == "Buy" or act == "Add":
					new_row_buy.append([gurus_name]+list(row))
				else:
					new_row_sell.append([gurus_name]+list(row))
	
	df_buy = pd.DataFrame(new_row_buy, columns = ['Gurus','Symbol', 'Date', 'Action', 'Comment', 'Shares', 'Price'])
	df_buy.to_csv("data/symbol/{0}_gurus_buy_{1}.csv".format(sector, date), index = None)
	df_sell = pd.DataFrame(new_row_sell, columns = ['Gurus','Symbol', 'Date', 'Action', 'Comment', 'Shares', 'Price'])
	df_sell.to_csv("data/symbol/{0}_gurus_sell_{1}.csv".format(sector, date), index = None)

if __name__ == '__main__':
	# name = 'George+Soros'
	name = 'Paul+Singer'
	# name = 'Warren+Buffett'
	## action: "Add", "Buy", "Sold Out", "Reduce"

	this_date = '2017-12-31'
	
	# for name in ['Warren+Buffett', 'George+Soros', 'Bruce+Berkowitz', "Seth+Klarman", "David+Tepper", "John+Paulson", \
	# 			"David+Einhorn", "Mohnish+Pabrai", "Prem+Watsa", "Bill+Ackman", "Joel+Greenblatt", \
	# 			"Carl+Icahn", "Arnold+Schneider", "Arnold+Van+Den+Berg", "Bill+Gates", \
	# 			"Bill+Nygren"]:
	# 	scrape_gurus(name, this_date = '2017-12-31')
	scrape_gurus(name, this_date = '2017-12-31')
	# filter_gurus(date = this_date, sector = 'tech', extend_list = ['BABA', 'AMZN'])

	# filter_gurus(date = this_date, sector = 'tech')
