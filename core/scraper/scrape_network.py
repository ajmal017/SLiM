import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob
import time
import numpy as np
import os.path
from datetime import datetime

def clean_text(txt):
	txt = txt.replace(',','')
	txt = txt.replace(' ','')
	txt = txt.replace('\n','')

	return txt

def scrape_competitor_symbol(symbol):
	urlHead = 'http://financials.morningstar.com/cmpind/competitors/industry-peer-data.action?'
	soup = BeautifulSoup(requests.get(urlHead+'t='+symbol).content, 'lxml')
	tables = soup.find_all('table')
	trs = tables[1].find_all("tr")
	fn = 'data/competitor/{0}_comp.csv'.format(symbol)
	data = []
	for tr in trs[1:]:
		content = tr.find('a')
		if content:
			try:
				tds = tr.find_all('td')
				if len(tds) == 11:
					mcap = clean_text(tds[1].text)
					net = clean_text(tds[2].text)
				else:
					mcap = 0
					net = 0
				name = content.text
				link = content.get('href')
				title = BeautifulSoup(requests.get('https:'+link).content,'lxml').find('title')
				ticker = title.text.split(' ')[0]
				data.append([ticker, name, mcap, net])
			except ValueError as err:
				print 'fail: ' + repr(err)
	avg = trs[-2].find_all('td')
	mcap_avg = clean_text(avg[1].text)
	net_avg = clean_text(avg[2].text)
	data.append(['Industrial Average', '', mcap_avg, net_avg])
	df = pd.DataFrame(data, columns = ['Symbol', 'Name', 'market cap', 'net income'])
	df.to_csv(fn, index = None)



# import networkx as nx
# from networkx.algorithms import bipartite
# https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.bipartite.html
# B = nx.Graph()
# B.add_nodes_from([1,2,3,4], bipartite=0) # Add the node attribute "bipartite"
# B.add_nodes_from(['a','b','c'], bipartite=1)
# B.add_edges_from([(1,'a'), (1,'b'), (2,'b'), (2,'c'), (3,'c'), (4,'a')])

# B.add_nodes_from(a, bipartite=1)
# B.add_nodes_from(b, bipartite=0)
# X, Y = bipartite.sets(B)
# pos = dict()
# pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
# pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
# nx.draw(B, pos=pos)
# nx.draw(B, with_labels = True)  
# plt.show()


if __name__ == '__main__':
	symbol = 'AMBA'
	scrape_competitor_symbol(symbol)