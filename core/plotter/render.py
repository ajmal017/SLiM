import pandas as pd 

def img2html_symbol_list(symbol_source, date, types_, price_from = 'Close'):
	# types_: candle, ewma_volume
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	title = '{0}_{1}'.format(symbol_source, date)
	fn = 'report/{0}.html'.format(title)

	with open(fn, 'w') as f:
		f.write('<!DOCTYPE html>\n')
		f.write('<html><head><title>{0}</title></head><body><center>\n'.format(title))
		for symbol in symbol_list:
			f.write('<h2>{0}</h2>\n'.format(symbol))
			for type_ in types_:
				# f.write('<img src="../data/plot/{0}/{0}_{1}_{2}_{3}.png">\n'.format(date, type_, symbol, price_from))
				f.write('<img src="../data/plot/{0}/{0}_{1}_{2}.png" width="800" height="600">\n'.format(date, type_, symbol))

		f.write('</center></body></html>')
	print("report saved to {0}".format(fn))


def render_price_plot(symbol_source, date, type_, price_from):
	# type_: short_sma, short_ewma, long_sma, long_ewma
	symbol_list = pd.read_csv('data/symbol/{0}.csv'.format(symbol_source))['Symbol']
	title = '{0}_{1}_{2}_{3}'.format(symbol_source, type_, price_from, date)
	# os.remove('/static/*.png')
	
	text = ""
	text += '<!DOCTYPE html>\n'
	text += '<html><head><title>{0}</title></head><body><center>\n'.format(title)
	# copyfile(src, dst)

	for symbol in symbol_list:
		text += '<h2>{0}</h2>\n'.format(symbol)
		text += '<img src="/data/plot/{0}/{0}_{1}_{2}_{3}.png">\n'.format(date, type_, symbol, price_from)
	text += '</center></body></html>'
	return text
