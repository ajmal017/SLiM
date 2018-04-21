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
			if growth_revenue != 'key error':
				if float(growth_revenue) < 0.1:
					return
			if growth_earning != 'key error' and float(growth_earning) < 0.2:
				return
			
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
			# book_value = __try_catch_dict(result['defaultKeyStatistics']['bookValue'], 'fmt')
			float_shares = __try_catch_dict(result['defaultKeyStatistics']['floatShares'], 'fmt')
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'fmt')
			ev2ebita = __try_catch_dict(result['defaultKeyStatistics']['enterpriseToEbitda'], 'raw')			
			fPE = __try_catch_dict(result['defaultKeyStatistics']['forwardPE'], 'fmt')

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
					print(item['date'], item['earnings']['fmt'], item['revenue']['fmt'])
				except:
					continue
			print("---- quarterly Earning&Revenue ----")
			for item in earn_quar:
				try:
					print(item['date'], item['earnings']['fmt'], item['revenue']['fmt'])
				except:
					continue
			print('==== EPS Chart ====')
			for item in eps_quar:
				print(item['date'], item['actual']['fmt'])
			
			print('==== Investment Assessment ====')
			print("Analyst Number: ", analyst_num)
			print("Current Price: ", price_current)
			print("ebitda: ", ebitda)
			print("totalDebt: ", total_debt)
			print("freeCashflow: ", fcf)
			print("earningsGrowth: ", growth_earning)
			print("revenueGrowth: ", growth_revenue)
			print('==== Key Statistics ====')
			print("Enterprise Value: ", enterprise_value)
			# print("Book Value: ", book_value)
			print("Market Cap: {0}/{1} * {2}".format(float_shares, out_shares, price_current))
			print("EV/ebitda: ", ev2ebita)
			print("forward PE: ", fPE)
			print('==== Business Brief ====')
			print("Sector: ", sector)
			print("Employee Number: ", empl_num)
			print("Business: ", business.encode('utf-8'))
			# with open("business_text.txt", 'a+') as f2:
			# 	f2.write(business.encode('utf-8'))
			print("#####################################\n")
		
	except Exception as err:
		print("########### {0} ############".format(symbol))
		print(repr(err))
		print("#####################################\n\n")
		# pass

def parse_json2txt_short_symbol(symbol, sector = 'tech'):
	file_ = 'data/json/{1}/all_{0}.json'.format(symbol, sector)
	
	if not os.path.exists(file_):
		return
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			growth_earning = __try_catch_dict(result['financialData']['earningsGrowth'], 'raw')
			growth_revenue = __try_catch_dict(result['financialData']['revenueGrowth'], 'raw')
			
			earnings = result['earnings'] #'financialsChart', 'earningsChart'
			earn_year = earnings['financialsChart']['yearly']
			earn_quar = earnings['financialsChart']['quarterly']
			eps_quar = earnings['earningsChart']['quarterly']
			ebitda = __try_catch_dict(result['financialData']['ebitda'], 'fmt')
			ev2ebita = __try_catch_dict(result['defaultKeyStatistics']['enterpriseToEbitda'], 'raw')			
			fPE = __try_catch_dict(result['defaultKeyStatistics']['forwardPE'], 'fmt')
			tPS = result['defaultKeyStatistics']['priceToSalesTrailing12Months']
			beta = result['defaultKeyStatistics']['beta']
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'fmt')

			price_current = __try_catch_dict(result['financialData']['currentPrice'], 'raw')
			business = __try_catch_dict(result['summaryProfile'], 'longBusinessSummary')
			roe = __try_catch_dict(result['financialData']['returnOnEquity'], 'fmt')
			roa = __try_catch_dict(result['financialData']['returnOnAssets'], 'fmt')
			fcf = __try_catch_dict(result['financialData']['freeCashflow'], 'fmt')
			

			profit_margins = __try_catch_dict(result['financialData']['profitMargins'], 'fmt')
			ebitda_margins = __try_catch_dict(result['financialData']['ebitdaMargins'], 'fmt')
			oper_margins = __try_catch_dict(result['financialData']['operatingMargins'], 'fmt')

			print("########### {0} ############".format(symbol))
			print('==== Financials Chart ====')
			print("---- yearly Earning&Revenue ----")
			for item in earn_year:
				try:
					print(item['date'], item['earnings']['fmt'], item['revenue']['fmt'])
				except:
					continue
			print("---- quarterly Earning&Revenue ----")
			for item in earn_quar:
				try:
					print(item['date'], item['earnings']['fmt'], item['revenue']['fmt'])
				except:
					continue
			print('==== EPS Chart ====')
			for item in eps_quar:
				print(item['date'], item['actual']['fmt'])
			
			print('==== Key Statistics ====')
			print("Current Price: ", price_current)
			print("earningsGrowth: ", growth_earning)
			print("revenueGrowth: ", growth_revenue)
			print("ebitda: ", ebitda)
			print("freeCashflow: ", fcf)
			print("EV/ebitda: ", ev2ebita)
			print("forward P/E: ", fPE)
			print("trailing P/S: ", tPS)
			print("Market Cap: {0} * {1}".format(out_shares, price_current))
			print("EV/ebitda: ", ev2ebita)
			print("ROE: ", roe)
			print("ROA: ", roa)
			
			print("operating margins", oper_margins)
			print("ebitda margins", ebitda_margins)
			print("profit margins", profit_margins)

			print("Business: ", business.encode('utf-8'))
			print("#####################################\n")

	except Exception as err:
		print("########### {0} ############".format(symbol))
		print(repr(err))
		print("#####################################\n\n")


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
				print(symbol, ratio)
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
		print("{0}: json file not found".format(symbol))
		return None, None
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			roe = __try_catch_dict(result['financialData']['returnOnEquity'], 'fmt')
			roa = __try_catch_dict(result['financialData']['returnOnAssets'], 'fmt')
			
			print("[{0}] roe: {1} roa: {2}".format(symbol, roe, roa))
			return roe, roa

	except Exception as err:
		return None, None

def parse_roe_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	# symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		parse_roe_symbol(symbol)

def parse_investor_symbol(symbol):
	file_ = 'data/json/tech/all_{0}.json'.format(symbol)
	if not os.path.exists(file_):
		print("{0}: json file not found".format(symbol))
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
		print(repr(err))
		# pass
	# with open(output_file) as f:
	# 	for pair in pairlist:
	# 		f.write(pair)
	# 		f.write('\n')
	for pair in pairlist:
		print(pair)

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
		print(repr(err))
		print("failed on " + file_)

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

def make_report_symbol_list(symbol_source, short = True):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		if not short:
			parse_json2txt_symbol(symbol, sector = symbol_source)
		else:
			parse_json2txt_short_symbol(symbol, sector = symbol_source)


def parse_cap_symbol(symbol):
	file_ = 'data/json/tech/all_{0}.json'.format(symbol)
	if not os.path.exists(file_):
		print("{0}: json file not found".format(symbol))
		return
	output_file = 'data/network_output/inv_sym_relation.txt'
	pairlist = []
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'raw')
			price_current = __try_catch_dict(result['financialData']['currentPrice'], 'raw')
			try: 
				cap = int(int(out_shares) * float(price_current))
			except:
				cap = None
			return cap
	except Exception as err:
		print(repr(err))
		print("failed on " + file_)
		return None

def split_by_cap(symbol_source):
	mini_cap = []
	small_cap = []
	mid_cap = []
	big_cap = []
	
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		cap = parse_cap_symbol(symbol)
		# print symbol, cap
		if not cap:
			continue
		mil_cap = cap / 1000000
		if mil_cap >= 10000:
			big_cap.append([symbol, mil_cap])
		elif mil_cap >= 2000:
			mid_cap.append([symbol, mil_cap])
		elif mil_cap >= 300:
			small_cap.append([symbol, mil_cap])
		else:
			mini_cap.append([symbol, mil_cap])
	pd.DataFrame(big_cap, columns = ['Symbol', 'Cap (in million)']).to_csv("data/symbol/{}_big_cap.csv".format(symbol_source), index = None)
	pd.DataFrame(mid_cap, columns = ['Symbol', 'Cap (in million)']).to_csv("data/symbol/{}_mid_cap.csv".format(symbol_source), index = None)
	pd.DataFrame(small_cap, columns = ['Symbol', 'Cap (in million)']).to_csv("data/symbol/{}_small_cap.csv".format(symbol_source), index = None)
	pd.DataFrame(mini_cap, columns = ['Symbol', 'Cap (in million)']).to_csv("data/symbol/{}_mini_cap.csv".format(symbol_source), index = None)


def parse_target_symbol(symbol, sector = 'tech'):
	file_ = 'data/json/{1}/all_{0}.json'.format(symbol, sector)
	
	if not os.path.exists(file_):
		print("no such file")
		return
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			price = __try_catch_dict(result['financialData']['currentPrice'], 'raw')
			target_mean = __try_catch_dict(result['financialData']['targetMeanPrice'], 'raw')
			num_analysts = __try_catch_dict(result['financialData']['numberOfAnalystOpinions'], 'raw')
			key = result['financialData']['recommendationKey']
			rise = round(float(target_mean) / float(price) - 1, 2)
			growth_earning = __try_catch_dict(result['financialData']['earningsGrowth'], 'raw')
			growth_revenue = __try_catch_dict(result['financialData']['revenueGrowth'], 'raw')
			fPE = __try_catch_dict(result['defaultKeyStatistics']['forwardPE'], 'fmt')
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'raw')
			peg = __try_catch_dict(result['defaultKeyStatistics']['pegRatio'], 'raw')

			cap = round(int(out_shares) * float(price) / 1000000000, 2) # in billion

			# if rise < 0.20 or growth_revenue < 0 or cap < 10:
			# 	return

			# if rise < 0.25 or growth_revenue < 0 or cap < 2 or cap > 10:
			# 	return

			if peg > 1 or growth_revenue < 0 or cap < 2:
				return

			print("########### {0} ############".format(symbol))
			print("current price: ", price)
			print("target mean: ", target_mean)
			print("growth (revenue/earning): ", growth_revenue, growth_earning)
			print("forward PE: ", fPE)
			print("peg ratio: ", peg)
			print("market cap (B): ", cap)
			print("rise up: ", rise)
			print("number of analysts: ", num_analysts)
			print("recommendation key: ", key)
	
	except Exception as err:
		# print("########### {0} ############".format(symbol))
		# print(repr(err))
		pass


def parse_target_symbol_list(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	symbol_list = list(set(symbol_list))
	for symbol in symbol_list:
		parse_target_symbol(symbol)

def magic_formula():
	pass

def parse_valuation_symbol(symbol, sector = 'watch'):
	file_ = 'data/json/{1}/all_{0}.json'.format(symbol, sector)
	
	if not os.path.exists(file_):
		print("no such file")
		return
	
	try:
		with open(file_) as f:
			data = json.load(f)
			result = data["quoteSummary"]["result"][0]
			
			### get growth ###
			growth_earning = __try_catch_dict(result['financialData']['earningsGrowth'], 'fmt')
			growth_revenue = __try_catch_dict(result['financialData']['revenueGrowth'], 'fmt')
			#######################

			### get margins ###
			gross_margins = __try_catch_dict(result['financialData']['grossMargins'], 'fmt')
			ebitda_margins = __try_catch_dict(result['financialData']['ebitdaMargins'], 'fmt')
			oper_margins = __try_catch_dict(result['financialData']['operatingMargins'], 'fmt')
			profit_margins = __try_catch_dict(result['financialData']['profitMargins'], 'fmt')
			#######################
			
			### get cash flow ###
			fcf = __try_catch_dict(result['financialData']['freeCashflow'], 'fmt')
			operating_cf = __try_catch_dict(result['financialData']['operatingCashflow'], 'fmt')		
			#######################
			
			### get price and shares ###
			price_current = __try_catch_dict(result['financialData']['currentPrice'], 'raw')
			out_shares = __try_catch_dict(result['defaultKeyStatistics']['sharesOutstanding'], 'raw')
			#######################
			
			### calculate market cap ###
			try: 
				cap = int(int(out_shares) * float(price_current))
			except Exception as err:
				print(repr(err))
				cap = None
			################################
			
			### calculate yearly revenue ###
			# revenues = []
			# earnings = []
			# year = []
			# earn_year = result['earnings']['financialsChart']['yearly']
			# for item in earn_year:
			# 	try:
			# 		year.append(item['date'])
			# 		revenues.append(item['revenue']['fmt'])
			# 		earnings.append(item['earnings']['fmt'])
			# 	except:
			# 		continue
			############################

			### calculate forward, trailing P/E ###
			trailingEps = __try_catch_dict(result['defaultKeyStatistics']['trailingEps'], 'raw')
			# forwardEps = __try_catch_dict(result['defaultKeyStatistics']['forwardEps'], 'raw')
			fPE = __try_catch_dict(result['defaultKeyStatistics']['forwardPE'], 'fmt')
			PE = round(price_current / trailingEps, 2)
			# fPE2 = price_current / forwardEps
			# print(fPE, fPE2, PE)
			############################

			### calculate trailing P/S ###
			try: 
				total_revenue = __try_catch_dict(result['financialData']['totalRevenue'], 'raw')
				PS = cap / total_revenue
			except:
				PS = 0
			############################

			### merge all metrics ###		
			row = [ symbol, price_current,  cap/1000000000,
					PS, PE,
					gross_margins, ebitda_margins, oper_margins, profit_margins,
					growth_revenue, growth_earning, 
					fcf, operating_cf]
			############################
			return row
	
	except Exception as err:
		# print("########### {0} ############".format(symbol))
		print(symbol, repr(err))
			
def make_valuation_matrix(symbol_source):
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	
	column_names = ['symbol', 'price', 'market cap(B)', 'P/S', 'P/E', 
					'gross margins', 'ebitda margins', 'operating margins', 'profit_margins',
					'growth revenue', 'growth earning',
					'free cash flow', 'operating cash flow']
	
	df = []
	for symbol in symbol_list:
		row = parse_valuation_symbol(symbol, sector = symbol_source)
		# print(row)
		if row and len(row) == len(column_names):
			df.append(row)
	data = pd.DataFrame(df, columns = column_names)
	print(data.shape)
	data.to_csv('data/watch_valuation.csv', index = None)


if __name__=='__main__':
	
	# COLS = []
	# with open('key.txt') as f:
	# 	COLS = [line.rstrip() for line in f if line[0]!='-']
	# print COLS
	# row = parse_json2mat_symbol('tech', 'AMD', COLS)
	# make_matrix_sector('tech', COLS)
	# make_matrix_sector('health', COLS)
	
	# parse_json2txt_symbol('ADBE')
	# make_report_symbol_list('semi', short = True)
	# check_float_out_ratio('tech')
	# parse_investor_symbol('NVDA')
	# parse_investor_symbol_list('hold')
	
	# parse_roe_symbol_list('research_up_last_year')

	# split_by_cap('tech')

	# parse_target_symbol_list('tech')
	# parse_valuation_symbol('NVDA')
	make_valuation_matrix('watch')