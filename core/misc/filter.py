import pandas as pd 
import glob



def filter_report_list():
	files_ = glob.glob('../symbol/report_*.csv')
	s = []
	tech = list(pd.read_csv('../symbol/tech.csv')['Symbol'])
	for f in files_:
		data = pd.read_csv(f)
		l = list(data['Symbol'])
		s += l

	with open('../symbol/report_in_tech.csv', 'w') as f:
		f.write('Symbol\n')
		for symbol in s:
			if symbol in tech:
				f.write(symbol + '\n')

if __name__ == '__main__':
	filter_report_list()