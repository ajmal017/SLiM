import argparse

def num2str(num):
	int_, float_ = str(num).split('.')
	in_str = list(int_)
	out_str = in_str[::]
	for i in range(0, len(in_str), 3):
		# print i, len(in_str) - i
		if i != 0:
			out_str.insert(len(in_str) - i, ',')
	
	return '.'.join([''.join(out_str), float_])

def snowball(money, rate, year):
	before = num2str(round(money,2))

	for i in range(year):
		money *=(1+rate)

	after = num2str(round(money,2))
	print money
	print "yearly rate {2} \nstart money: {0} \nyears: {1} \nreturn: {3}".format(before, year, rate, after)

parser = argparse.ArgumentParser()
parser.add_argument("-m", type = float, help="add money")
parser.add_argument("-r", type = float, help="add rate")
parser.add_argument("-y", type = int, help="add year")


args = parser.parse_args()
m = args.m
r = args.r
y = args.y

snowball(money = m, rate = r, year = y)