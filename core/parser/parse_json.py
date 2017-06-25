import pandas as pd 
import json
import glob
import os.path
import collections
import datetime

def __try_catch_dict(dict_, key):
	try:
		return dict_[key]
	except:
		return "key error"

def parse_json2txt_symbol(symbol, sector = 'tech'):
	file_ = 'data/json/{1}/all_{0}.json'.format(symbol, sector)
	
	if not os.path.exists(file_):
		return
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]

			growth_earning = __try_catch_dict(result['financialData']['earningsGrowth'], 'raw')
			growth_revenue = __try_catch_dict(result['financialData']['revenueGrowth'], 'raw')
			# if growth_revenue == 'key error' or growth_earning == 'key error':
			# 	return
			# if growth_revenue != 'key error':
			# 	if float(growth_revenue) < 0.1:
			# 		return
			# if growth_earning != 'key error' and float(growth_earning) < 0.2:
			# 	return
			
			price_current = __try_catch_dict(result['financialData']['currentPrice'], 'raw')
			# if float(price_current) > 10:
			# 	return

			rec_key = __try_catch_dict(result['financialData'], 'recommendationKey')
			# if rec_key != 'strong_buy':
			# 	return

			sector = __try_catch_dict(result['summaryProfile'], 'sector')
			business = __try_catch_dict(result['summaryProfile'], 'longBusinessSummary')
			empl_num = __try_catch_dict(result['summaryProfile'], 'fullTimeEmployees')
			enterprise_value = __try_catch_dict(result['defaultKeyStatistics']['enterpriseValue'], 'fmt')
			book_value = __try_catch_dict(result['defaultKeyStatistics']['bookValue'], 'fmt')
			float_shares = __try_catch_dict(result['defaultKeyStatistics']['floatShares'], 'fmt')
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'fmt')
			ev2ebita = __try_catch_dict(result['defaultKeyStatistics']['enterpriseToEbitda'], 'raw')			
			
			ebitda = __try_catch_dict(result['financialData']['ebitda'], 'fmt')
			analyst_num = __try_catch_dict(result['financialData']['numberOfAnalystOpinions'], 'raw')
			total_debt = __try_catch_dict(result['financialData']['totalDebt'], 'fmt')
			fcf = __try_catch_dict(result['financialData']['freeCashflow'], 'fmt')
			
			earnings = result['earnings'] #'financialsChart', 'earningsChart'
			earn_year = earnings['financialsChart']['yearly']
			earn_quar = earnings['financialsChart']['quarterly']
			eps_quar = earnings['earningsChart']['quarterly']
			
		
			print("########### {0} ############".format(symbol))
			print('==== Financials Chart ====')
			print("---- yearly Earning&Revenue ----")
			for item in earn_year:
				try:
					print item['date'], item['earnings']['fmt'], item['revenue']['fmt']
				except:
					continue
			print("---- quarterly Earning&Revenue ----")
			for item in earn_quar:
				try:
					print item['date'], item['earnings']['fmt'], item['revenue']['fmt']
				except:
					continue
			print('==== EPS Chart ====')
			for item in eps_quar:
				print item['date'], item['actual']['fmt']
			
			print('==== Investment Assessment ====')
			print "Analyst Number: ", analyst_num
			print "Current Price: ", price_current
			print "ebitda: ", ebitda
			print "totalDebt: ", total_debt
			print "freeCashflow: ", fcf
			print "earningsGrowth: ", growth_earning
			print "revenueGrowth: ", growth_revenue
			print('==== Key Statistics ====')
			print "Enterprise Value: ", enterprise_value
			print "Book Value: ", book_value
			print "Market Cap: {0}/{1} * {2}".format(float_shares, out_shares, price_current)
			print "EV/ebitda: ", ev2ebita
			print('==== Business Brief ====')
			print "Sector: ", sector
			print "Employee Number: ", empl_num
			print "Business: ", business.encode('utf-8')
			# with open("business_text.txt", 'a+') as f2:
			# 	f2.write(business.encode('utf-8'))
			print("#####################################\n")
		
	except Exception as err:
		print("########### {0} ############".format(symbol))
		print repr(err)
		print("#####################################\n\n")
		# pass

def check_float_out_ratio(symbol_source):

	def _check_symbol(symbol):
		file_ = 'data/json/tech/all_{0}.json'.format(symbol)
		if not os.path.exists(file_):
			file_ = 'data/json/health/all_{0}.json'.format(symbol)
			if not os.path.exists(file_):
				return
		try:
			with open(file_) as f:
				data = json.load(f)
				result = data["quoteSummary"]["result"][0]
				float_shares = __try_catch_dict(result['defaultKeyStatistics']['floatShares'], 'raw')
				out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'raw')
				ratio = float(float_shares) / float(out_shares)
				print symbol, ratio
		except Exception as err:
			# print repr(err)
			pass

	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		_check_symbol(symbol)

def parse_roe_symbol(symbol):
	file_ = 'data/json/tech/all_{0}.json'.format(symbol)
	if not os.path.exists(file_):
		print "{0}: json file not found".format(symbol)
		return
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			roe = __try_catch_dict(result['financialData']['returnOnEquity'], 'fmt')
			roa = __try_catch_dict(result['financialData']['returnOnAssets'], 'fmt')
			print "[{0}] roe: {1} roa: {2}".format(symbol, roe, roa)
	except Exception as err:
		pass
def parse_roe_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	# symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		parse_roe_symbol(symbol)

def parse_investor_symbol(symbol):
	file_ = 'data/json/tech/all_{0}.json'.format(symbol)
	if not os.path.exists(file_):
		print "{0}: json file not found".format(symbol)
		return
	output_file = 'data/network_output/inv_sym_relation.txt'
	pairlist = []
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			history_list = result['upgradeDowngradeHistory']['history']
			#firm, action, epochGradeDate, fromGrade, toGrade
			for item in history_list:
				firm = item['firm']
				action = item['action']
				epoch = int(item['epochGradeDate'])
				date = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')
				if epoch > 1483228800:
					pair = ((firm, symbol),(action, date))
					pairlist.append(pair)
	except Exception as err:
		print repr(err)
		# pass
	# with open(output_file) as f:
	# 	for pair in pairlist:
	# 		f.write(pair)
	# 		f.write('\n')
	for pair in pairlist:
		print pair

def parse_investor_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	# symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		parse_investor_symbol(symbol)


def parse_json2mat_symbol(COLS, file_ = None, sector = None, symbol = None):
	if not file_:
		file_ = 'data/json/{0}/all_{1}.json'.format(sector, symbol)
	if not symbol:
		symbol = file_.split('_')[-1].split('.')[0]

	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			try:
				sector = result['summaryProfile']['sector']
			except:
				sector = None
			try:
				emp_num = result['summaryProfile']['fullTimeEmployees']
			except:
				emp_num = None
			financial_data = result['financialData']
			key_stats = result['defaultKeyStatistics']
			row = [symbol, sector, emp_num]
			for k in COLS[3:]:
				if k in financial_data.keys():
					try:
						if 'raw' in financial_data[k]:
							v = financial_data[k]['raw']
						else:
							v = financial_data[k]
					except:
						v = None
				elif k in key_stats.keys():
					try:
						if 'raw' in key_stats[k]:
							v = key_stats[k]['raw']
						else:
							v = key_stats[k]
					except:
						v = None
				else:
					v = None
				if str(v) == '{}':
					v = None
				row.append(v)
		return row

	except Exception as err:
		print repr(err)
		print "failed on " + file_

def make_matrix_sector(sector, COLS):
	files = glob.glob('data/json/{0}/all_*.json'.format(sector))
	data = []
	for file_ in files:
		r = parse_json2mat_symbol(COLS, file_, None, None)
		if r:
			data.append(r)
	df = pd.DataFrame(data, columns = COLS)
	# print df.shape
	# print df.head(2)
	df.to_csv('data/matrix/mat_{0}.csv'.format(sector), index = None)

def make_report_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		parse_json2txt_symbol(symbol)

if __name__=='__main__':
	
	# COLS = []
	# with open('key.txt') as f:
	# 	COLS = [line.rstrip() for line in f if line[0]!='-']
	# print COLS
	# row = parse_json2mat_symbol('tech', 'AMD', COLS)
	# make_matrix_sector('tech', COLS)
	# make_matrix_sector('health', COLS)
	
	# parse_json2txt_symbol('ADBE')
	# make_report_symbol_list('automotive')
	# check_float_out_ratio('tech')
	# parse_investor_symbol('NVDA')
	# parse_investor_symbol_list('hold')
	
	parse_roe_symbol_list('research_up_last_year')