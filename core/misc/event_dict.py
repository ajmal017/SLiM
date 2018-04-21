import pickle

fil = 'financial_calendar'

def load_calendar():
	cal = pickle.load(open(fil, 'rb'))
	return cal

def save_calendar(cal):
	pickle.dump(cal, open(fil, 'wb'))

def add_event(date, event):
	cal = load_calendar()
	if date not in cal.keys():
		cal[date] = []
		
	cal[date].append(event)
	save_calendar(cal)

def reset_calendar():
	cal = {}
	save_calendar(cal)

def print_calendar():
	cal = load_calendar()
	print cal

def add_event_batch(event_list):
	cal = load_calendar()
	for date, event in event_list:
		if date not in cal.keys():
			cal[date] = []
		cal[date].append(event)
	save_calendar(cal)

reset_calendar()
event_list = [('0725', 'AMD'), ('0727','SSNC')]
# add_event('0725', 'amd')
add_event_batch(event_list)
print_calendar()