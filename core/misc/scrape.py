#!/bin/python
# encoding=utf-8
import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
from bs4 import BeautifulSoup
import time
import pandas as pd 


#Take this class for granted.Just use result of rendering.
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  

def scraper(index):
	t1 = time.time()
	url = "https://xueqiu.com/S/{0}/keyratios".format(index)
	r = Render(url)  
	result = r.frame.toHtml()
	formatted_result = str(result.toUtf8())
	# formatted_result = str(result.toAscii())
	soup = BeautifulSoup(formatted_result, 'lxml')
	tables = soup.find_all("table")

	col_1 = []
	col_2 = []
	col_3 = []
	col_4 = []
	# col_0 = []
	for t in tables:
		body = t.find("tbody")
		trs = body.find_all("tr")[1:]
		for tr in trs:
			items = tr.find_all("td")
			if len(items) == 5:
				# col_0.append(items[0].contents[0])
				col_1.append(items[1].contents[0])
				col_2.append(items[2].contents[0])
				col_3.append(items[3].contents[0])
				col_4.append(items[4].contents[0])

	data = pd.DataFrame([col_1, col_2, col_3, col_4], columns = COLUMNS)
	t2 = time.time()
	print("{0} is finished scaping and saved to local with {1} seconds".format(index, (t2-t1)))

	# print data.shape
	data.to_csv("table/{0}.csv".format(index), index = None)
	# print col_0

def get_column_name():
	with open('names.txt') as f:
		x = f.read()
	x2 = x.split('\r\n')
	return x2

if __name__ == '__main__':
	index = 'NVDA'
	COLUMNS = get_column_name()
	# print COLUMNS
	scraper(index)

