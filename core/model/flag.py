## model parameters

DELTA_PAST_T = 30 # construct feature from past t days
DELTA_FUTURE_T = 30 # get price after future t days 
UP_RATE_TRHE = 0.04 # set buy signal if up rate is higher than threshold

CLUSTER_NUM = 4

XGB_DEP = 15
XGB_NUM_ROUND = 100
XGB_ETA = 0.01
XGB_SCORE_THRE = 0.7 

SEED = 50 # random split seed