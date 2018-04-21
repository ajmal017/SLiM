# -*- coding: utf-8 -*-
import json
import requests

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2",
    "Cache-Control": "no-cache",
   	"Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    ##"X-Requested-With": "XMLHttpRequest",
}
##Keep-Alive: 300
##Connection: keep-alive
##Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120
##Pragma: no-cache
##Cache-Control: no-cache

def scrape_cn_industry():
	size = 900
	for page in range(1,11):
		print "scraping page {}".format(page)
		json_link = 'https://xueqiu.com/stock/cata/stocklist.json?page={0}&size={1}&order=desc&orderby=pe_ttm&exchange=CN&plate='.format(page, size)

		json_response = requests.get(json_link, headers = headers)
		print json_response.text
		return
		json_loaded =  json.loads(json_response.text.encode('utf-8'))
		fn = "data/CN/CN_Stocklist_{}.json".format(page)
		with open(fn,'w') as f:
			json_loadedson.dump(json_loaded, f, indent = 4)

def scrape_cn_finance(symbol, sheet = 'incstatement'):
	url = 'https://xueqiu.com/stock/f10/{0}.json?symbol={1}&page=0&size=10000'.format(sheet, symbol)
	print url
	r = requests.get(url, headers = headers)
	if r.status_code == 200:
		print r.text
	else:
		print r.text
		print r.status_code
	return
	json_loaded =  json.loads(r.text)

def scrape_cn_finance_main(symbol):

	url = 'http://quotes.money.163.com/hk/service/cwsj_service.php?symbol={0}&start=2006-06-30&end=2017-12-31&type=cwzb'.format(symbol)

	r = requests.get(url)
	if r.status_code == 200:
		for item in json.loads(r.text):
			year = item['YEAREND_DATE']
			eps = item['EPS']
			print year, eps

def scrape_cn_finance_lrb(symbol):
	url = 'http://quotes.money.163.com/hk/service/cwsj_service.php?symbol={0}&start=2006-06-30&end=2017-12-31&type=lrb'.format(symbol)
	r = requests.get(url)
	if r.status_code == 200:
		for item in json.loads(r.text):
			year = item['YEAREND_DATE']
			pbt = item['PBT']
			dps = item['DPS']
			net = item['NET_PROF']
			op = item['OPER_PROFIT']
			print year, pbt, dps, net, op

if __name__ == '__main__':
	# scrape_cn_industry()
	# scrape_cn_finance(symbol = 'SZ300212')
	# scrape_cn_finance_main(symbol = '00700')
	scrape_cn_finance_lrb(symbol = '00700')