

import json
import pandas as pd
import numpy as np
from gensim.models import word2vec
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM, TimeDistributed, RepeatVector
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding
import sys
import csv
import emoji
import jieba
import keras

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import jieba.analyse

website={'udn','ltn','chinatimes','appledaily','tvbs'}
Q1={'udn','ltn','tvbs','chinatimes'}#支持通姦除罪(不明顯
Q2={'tvbs','ltn',}#取消機車待轉(都模糊)
Q3={'udn','tvbs','ltn'}#支持博弈特區(不明顯)
Q4={'appledaily','udn','tvbs'}#支持華航罷工(tvbs，不確定)
Q5={'ltn','tvbs','udn','chinatimes','appledaily'}#支持性交易 全支持???
Q6={'chinatimes','udn','appledaily','tvbs'}#ecfa
Q7={'ltn','udn','tvbs','appledaily','chinatimes'}#證所稅廢除
Q8={'ltn','tvbs','appledaily'}#贊成中油在觀塘興建第三天然氣接收站
Q9={'ltn','udn','chinatimes','tvbs','appledaily'}#陸生納保
Q10={'ltn','appledaily','udn','tvbs','chinatimes'}#服儀解禁
Q11={'chinatimes','ltn','appledaily'}#不支持使用加密貨幣(ltn態度模糊)
Q12={'udn','chinatimes','tvbs'}#不支持學雜費調漲(本項建議增加反對詞的權重)每個媒體都模糊
Q13={'ltn','tvbs'}#支持舉債前瞻
Q14={'chinatimes','ltn','udn','tvbs','appledaily'}#支持電競列入體育競技
Q15={'tvbs','udn','chinatimes','appledaily'}#返台鐵東移(ltn模糊)
Q16={'tvbs','ltn',}#支持陳前總統保外就醫(tvbs 模糊)
Q17={'ltn','appledaily'}#年改 取消18%
Q18={'udn','chinatimes'}#同意動物實驗(可刪，都不太支持)
Q19={'ltn','udn'}#油價應該凍漲或緩漲
Q20={'tvbs','appledaily','ltn'}#反對旺旺中時併購中嘉

url2index={}
count=0
index2website={}
with open('NC_1.csv', newline='') as csvFile:
#with open('/Users/peter yang/Downloads/train.csv', newline='') as csvFile:
	rows = csv.reader(csvFile, delimiter=',')
	for row in rows:
		if count==0:
			count+=1
			continue
		url2index[row[1]]=row[0]
		count+=1
		trans=row[1].replace('.','/')
		templist=trans.split('/')
		find =False
		for value in templist:
			for web in website:
				if(value==web):
					find=True
					break
			if(find==True):
				index2website[row[0]]=value
				count+=1
				break
		if find==False:
			print('error')
			print(row[1])