import nltk
import collections
import string
from nltk.stem.porter import *
from nltk.corpus import stopwords

stemmer = nltk.stem.snowball.SnowballStemmer('german')
stopwordlist = stopwords.words('english')
# stemmer = PorterStemmer()
my_filter = ['business', 'based', 'Inc.', 'Corporation', 'corporation', 'company', 'also', 'headquartered', 'founded', 'well', 'including', 'include', 'used', 'addition', 'offers', 'sells', 'sales', 'provides', 'name']

with open("text/tech_watch_text.txt") as f:
	text = f.read()

tes = text.replace('-',' ')
tokens = nltk.word_tokenize(tes)

tokens_filter = [i.lower() for i in tokens if i not in string.punctuation and i.lower() not in stopwordlist and i not in my_filter]
# print string.punctuation

tokens_stemmed = tokens_filter
# tokens_stemmed = [stemmer.stem(word) for word in tokens_filter]

fdist = nltk.FreqDist(tokens_stemmed)

with open('text_output/tech_watch_top_words.txt', 'w') as f:
	for word, frequency in fdist.most_common(200):
		try:
			f.write('{}:{}\n'.format(word.decode('utf-8'), frequency))
		except:
			pass