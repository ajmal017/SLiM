import core.scraper.scrape_finance as sf
import core.scraper.scrape_rss as sr 
import core.scraper.scrape_price as sp
import core.plotter.ts_plot as tplt
import core.plotter.render as plrd
import core.plotter.candle_plot as cplt
import core.parser.parse_json as pj
from datetime import datetime

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
	
	tplt.plot_price_volume_symbol_list(ph['symbol_source'], date = d, override = ph['override_plot'])
	# cplt.plot_candle_symbol_list(ph['symbol_source'], date = d)

	plrd.img2html_symbol_list(ph['symbol_source'], date = d, types_ = ['ewma_volume'])
################################################


############## interface monitor ######################
ph = {
	'symbol_source': 'watch',
	'date': None,
	'price_source': 'yahoo',
	'year': 3,
	'override_price': True,
	'override_plot': True,
	'price_type': 'Close'
}

interface_price_and_plot(ph)

# lod: list of date
# lod = map(lambda x:str(x).zfill(4), range(1029,1031))
# lod =  map(lambda x:str(x).zfill(4), range(428,430)) + map(lambda x:str(x).zfill(4), range(501,503))

# interface_rss_and_push(ph = {'source_from':'hold', 'rss_date': '11_01', 'since_date': '171029'})
################################################


