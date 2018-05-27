import core.scraper.scrape_finance as sf
import core.scraper.scrape_rss as sr 
import core.scraper.scrape_price as sp
import core.plotter.ts_plot as tplt
import core.plotter.render as plrd
import core.plotter.candle_plot as cplt
import core.parser.parse_json as pj
from datetime import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source",  type = str, help="to specify source of symbols")
parser.add_argument("--year", type = int, default = 2, help = "to specify year(s) of history price, default is 2 years")
parser.add_argument("--date", type = str, help = "to specify last date of history price, default is today")
parser.add_argument("--override_plot", action = "store_true", default = False, help = "to specify whether override plot, default is False")
parser.add_argument("--override_price", action = "store_true", default = False, help = "to specify whether override price, default is False")
parser.add_argument("--report", action = "store_true", default = False, help = "to specify whether report, default is False")

args = parser.parse_args()
################################################
############## scrape report list ###########
# sf.scrape_report_weekly(p1 = '2017-10-15', p2 = '2017-10-21')

############## scrape finance data #########
# sf.scrape_finance_summary_symbol('AMD')
# sf.scrape_finanace_summary_list('tech')
# sf.scrape_finance_all_symbol('AMD')
# sf.scrape_finance_all_list('health')
################################################

############## scrape rss #######################
# sr.scrape_rss_symbol('^IXIC', 'x')

def interface_rss_and_push(ph):
	sr.scrape_rss_list(source_from = ph['source_from'], rss_date = ph['rss_date'])
	sr.push_rss_html(source_from = ph['source_from'], rss_date = ph['rss_date'], since_date = ph['since_date'], report = True)
################################################


############## scrape price and ts plot ############
s = 'VGT'
# sp.scrape_price_symbol(s)
# tplt.plot_price_volume_symbol(symbol = s, date = '08_20', price_type = 'Close')

def interface_price_and_plot(ph):
	d = datetime.strftime(datetime.now(), '%m_%d') if not ph['date'] else ph['date']
	if not ph['date']:
		sp.scrape_price_symbol_list(ph['symbol_source'], ph['price_source'], ph['year'], ph['override_price'])
	
	# tplt.plot_price_volume_symbol_list(ph['symbol_source'], date = d, override = ph['override_plot'])
	# tplt.plot_rsi_symbol_list(ph['symbol_source'], date = d, override = ph['override_plot'])
	tplt.plot_price_rsi_symbol_list(ph['symbol_source'], date = d, override = ph['override_plot'])
	# cplt.plot_candle_symbol_list(ph['symbol_source'], date = d)
	if args.report:
		plrd.img2html_symbol_list(ph['symbol_source'], date = d, types_ = ['price_rsi'])
################################################


############## interface monitor ######################
ph = {
	'symbol_source': args.source,
	'date': args.date,
	'price_source': 'yahoo',
	'year': args.year,
	'override_price': args.override_price,
	'override_plot': args.override_plot,
	'price_type': 'Close'
}

interface_price_and_plot(ph)

# lod: list of date
# lod = map(lambda x:str(x).zfill(4), range(1029,1031))
# lod =  map(lambda x:str(x).zfill(4), range(428,430)) + map(lambda x:str(x).zfill(4), range(501,503))

# interface_rss_and_push(ph = {'source_from':'hold', 'rss_date': '11_01', 'since_date': '171029'})
################################################


