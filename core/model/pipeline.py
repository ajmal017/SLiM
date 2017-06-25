import pandas as pd 
import numpy as np 
import glob
import xgboost as xgb
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import collections
import matplotlib.pyplot as plt

from flag import *


def make_matrix_each(filename, delta_past_t = DELTA_PAST_T, delta_future_t = DELTA_FUTURE_T, thre = UP_RATE_TRHE):
	data = pd.read_csv(filename)
	price = np.array(data['Close'])[::-1]
	
	# ewma_5 = pd.ewma(price, span = 5, adjust = False)
	ewma_10 = pd.ewma(price, span = 10, adjust = False)
	ewma_20 = pd.ewma(price, span = 20, adjust = False)
	# ts_510 = (ewma_5 - ewma_10) / ewma_10
	ts_1020 = (ewma_10 - ewma_20) / ewma_20

	row = []
	for i in range(delta_past_t, len(price) - delta_future_t):
		# X1 = list(ts_510[(i - delta_past_t) : i])
		X2 = list(ts_1020[(i - delta_past_t) : i])
		# X = X1 + X2
		X = X2
		Y = (price[i + delta_future_t] - price[i])/price[i]
		if Y > thre:
			row.append(X + [1])
		else:
			row.append(X + [0])

	df = pd.DataFrame(row)
	return df


def make_matrix_batch(loc = '../price/04_06/*.csv'):
	print("processing matrix from batch {0}".format(loc))
	fs = glob.glob(loc)
	frame = []
	for i in range(len(fs)):
		if i%100 == 0:
			print("processing batch {0}".format(i))
		fn = fs[i]
		df = make_matrix_each(fn)
		frame.append(df)

	DF = pd.concat(frame)
	return DF
	# print DF.shape
	# print(sum(DF.iloc[:,10]>0))
def con_max(mat):
	print(mat)
	tp = mat[1][1]
	tn = mat[0][0]
	fp = mat[0][1]
	fn = mat[1][0]
	recall = tp*1.0 / (tp + fn)
	precision = tp*1.0 / (tp + fp)
	print("recall: {0}, precision: {1}".format(recall, precision))


def train_test_xgboost(Data):
	print("applying model xgboost")
	X = np.array(Data.iloc[:,:-1])
	y = np.array(Data.iloc[:,-1])
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state = SEED)

	dtrain = xgb.DMatrix(X_train, label = y_train)
	dtest = xgb.DMatrix(X_test)
	param = {'max_depth':XGB_DEP, 'eta':XGB_ETA, 'silent':1, 'objective':'binary:logistic' }
	num_round = XGB_NUM_ROUND
	plst = param.items()
	bst = xgb.train( plst, dtrain, num_round )
	# plt.scatter(y_test, bst.predict(dtest))
	# plt.show()
	pred_train = [1 if x > XGB_SCORE_THRE else 0 for x in bst.predict(dtrain)]
	pred_test = [1 if x > XGB_SCORE_THRE else 0 for x in bst.predict(dtest)]
	# mat_train = confusion_matrix(y_train, pred_train)
	# con_max(mat_train)
	mat_test = confusion_matrix(y_test, pred_test)
	con_max(mat_test)


def train_test_sklearn(Data):
	X = np.array(Data.iloc[:,:-1])
	y = np.array(Data.iloc[:,-1])
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state = 1)
	classifiers = [
	    # KNeighborsClassifier(3),
	    # SVC(kernel="linear", C=0.025),
	    # SVC(gamma=2, C=1),
	    # GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
	    # DecisionTreeClassifier(max_depth=5),
	    # MLPClassifier(alpha=1),
	    # AdaBoostClassifier(),
	    # GaussianNB(),
	    # QuadraticDiscriminantAnalysis(),
	    RandomForestClassifier(max_depth=5, n_estimators=20)
	    ]
	for m in classifiers:
		print("applying model {0}".format(m.__class__.__name__))
		m.fit(X_train, y_train)
		m_pred_train = m.predict(X_train)
		m_pred_test = m.predict(X_test)
		# mat_train = confusion_matrix(y_train, m_pred_train)
		# con_max(mat_train)
		mat_test = confusion_matrix(y_test, m_pred_test)
		con_max(mat_test)

def predict_clusering(Data, k = CLUSTER_NUM):
	X = np.array(Data.iloc[:,:-1])
	y = np.array(Data.iloc[:,-1])
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 100)

	kmeans = KMeans(n_clusters=k, random_state=0).fit(X_train)

	pred_labels_train = kmeans.predict(X_train)
	pred_labels_test = kmeans.predict(X_test)
	re_train = collections.Counter(zip(pred_labels_train, y_train))
	re_test = collections.Counter(zip(pred_labels_test, y_test))
	
	for i in range(k):
		print "cluser i: " + str(i)
		print(re_train[(i,1)]*1.0 / (re_train[(i,1)] + re_train[(i,0)]))
		print(re_test[(i,1)]*1.0 / (re_test[(i,1)] + re_test[(i,0)]))
	# print collections.Counter(re_test)
	new_label_test = list(map(lambda x: x[1]*10+x[0], zip(pred_labels_test, y_test)))
	pca = PCA(n_components=3)
	pca.fit(X_train)
	print(pca.explained_variance_ratio_) 
	x_test_transformed = pca.transform(X_test)
	plt.scatter(x_test_transformed[:,0], x_test_transformed[:,1], c = new_label_test)
	plt.show()

DF = make_matrix_batch(loc = '../price/04_22/*.csv')
# predict_clusering(DF)
train_test_xgboost(DF)
# train_test_sklearn(DF)