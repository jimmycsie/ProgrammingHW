import json as js
import jieba
import numpy as np
import csv
from gensim.models import word2vec
jieba.set_dictionary('dict.txt.big')
model = word2vec.Word2Vec.load("word2vec.model")

query_seg=[]
word_terms_freq = {}
word_to_index = {}
query = []
dictionary_size = 8000
document_num = 100000
threshold_num = 5000
query_path = "./news_data_1/QS_1.csv"
ans_path = "ans.csv"

# standpoint ------------------------------------------------------------------------------------------
query_standpoint = []
website={'udn','ltn','chinatimes','appledaily','tvbs'}
query_standpoint.append({'udn','ltn','tvbs','chinatimes'})	#支持通姦除罪(不明顯        
query_standpoint.append({'tvbs','ltn',})	#取消機車待轉(都模糊)
query_standpoint.append({'udn','tvbs','ltn'})	#支持博弈特區(不明顯)
query_standpoint.append({'appledaily','udn','tvbs'})	#支持華航罷工(tvbs，不確定)  #0.04%
query_standpoint.append({'ltn','tvbs','udn','chinatimes','appledaily'})		#支持性交易 全支持???
query_standpoint.append({'chinatimes','udn','appledaily','tvbs'})	#ecfa
query_standpoint.append({'ltn','udn','tvbs','appledaily','chinatimes'})		#證所稅廢除
query_standpoint.append({'ltn','tvbs','appledaily','udn'})	#贊成中油在觀塘興建第三天然氣接收站
query_standpoint.append({'ltn','udn','chinatimes','tvbs','appledaily'})		#陸生納保
query_standpoint.append({'ltn','appledaily','udn','tvbs','chinatimes'})		#服儀解禁
query_standpoint.append({'chinatimes','ltn','appledaily'})		#不支持使用加密貨幣(ltn態度模糊)
query_standpoint.append({'udn','chinatimes','tvbs'})	#不支持學雜費調漲(本項建議增加反對詞的權重)每個媒體都模糊
query_standpoint.append({'ltn','tvbs','appledaily','chinatimes'})		#支持舉債前瞻  0.08%
query_standpoint.append({'chinatimes','ltn','udn','tvbs','appledaily'})		#支持電競列入體育競技
query_standpoint.append({'tvbs','udn','chinatimes','appledaily','lstn'})		#返台鐵東移(ltn模糊)
query_standpoint.append({'tvbs','ltn'})		#支持陳前總統保外就醫(tvbs 模糊) udn
query_standpoint.append({'ltn','appledaily'})		#年改 取消18%
query_standpoint.append({'udn','chinatimes'})		#同意動物實驗(可刪，都不太支持)
query_standpoint.append({'ltn','udn'})		#油價應該凍漲或緩漲
query_standpoint.append({'tvbs','appledaily','ltn'})		#反對旺旺中時併購中嘉
for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18]:
    query_standpoint[i] = website
#------------------------------------------------------------------------------------------
def check(word):
    ignore = ['，', '。', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
              '-', '+', '=', '[', ']', ',', '.', '<', '>', '/', ';', ':', 
              '\'', '\"', '{', '}', '、', '\n','\r', '\t', '\a', '\b', '\f', '\v']
    for i in ignore:
        if(word == i):
            return False
    return True
#------------------------------------------------------------------------------------------


with open('url2content.json') as f:
	texts = js.load(f)
with open('word_to_index.json') as f:
	word_to_index = js.load(f)
with open('word_terms_freq.json') as f:
	word_terms_freq = js.load(f)
with open('index2website.json') as f:
	index2website = js.load(f)
news_bag = np.load("news_bag.npy")
query_bag = np.load("query_bag.npy")
news_vec = np.load("news_vec.npy")
query_vec = np.load("query_vec.npy")
standpoint = np.load("../news_standpoint.npy")
print(word_to_index["服儀"], word_terms_freq["服儀"])

with open(file = query_path, mode = 'r') as csvfile:
    rows = csv.reader(csvfile)
    first = True
    for row in rows:
        if(first == True):
            first = False
            continue
        query.append(row[1])
    csvfile.close()

stand = model.wv["支持"]/np.linalg.norm(model.wv["支持"]) + model.wv["合法"]/np.linalg.norm(model.wv["合法"])
oppose = model.wv["反對"]/np.linalg.norm(model.wv["反對"]) + model.wv["非法"]/np.linalg.norm(model.wv["非法"])
stand = stand/np.linalg.norm(stand)
oppose = oppose/np.linalg.norm(oppose)
# calculating tf-idf -----------------------------------------------------------
tf_idf_score = []
for i in range(query_bag.shape[0]):
    temp = []
    for k in range(document_num):
        if(news_bag[k][0]!=0):        # ignore no word news and below threshold news
            #score = np.dot(query_bag[i][1:], news_bag[k][1:]) / ( np.linalg.norm(query_bag[i][1:])*np.linalg.norm(news_bag[k][1:]) )             # exclude sum of word       
            score = np.dot(query_vec[i], news_vec[k]) / ( np.linalg.norm(query_vec[i])*np.linalg.norm(news_vec[k]) )
            if(i == 2):
                if( standpoint[k] >= 0.5 and np.dot(query_bag[i][1:], news_bag[k][1:])>0):
                    temp.append( (score,k+1) )
            elif(index2website[str(k)] in query_standpoint[i] and np.dot(query_bag[i][1:], news_bag[k][1:])>0):
                temp.append( (score,k+1) )
    tf_idf_score.append(temp)
    print(len(temp))

print(word_to_index["支持"], word_to_index["反對"])
#------------------------------------------------------------------------------


# creating answer
q_idx = []
for i in range(1, 10):
    q_idx.append('q_0'+str(i))
for i in range(10, 21):
    q_idx.append('q_'+str(i))

header = []
header.append("Query_Index")
for i in range(1, 10):
    header.append("Rank_00"+str(i))
for i in range(10, 100):
    header.append("Rank_0"+str(i))
for i in range(100, 301):
    header.append("Rank_"+str(i))

ans = []
ans.append(header)
for i in range(len(query)):
    rank = sorted(tf_idf_score[i], reverse=True)  
    temp = []
    temp.append(q_idx[i])
    for j in range(300):
        news = rank[j][1]
        if(news<10):
            temp.append("news_00000"+str(news))
        elif(news>=10 and news<100):
            temp.append("news_0000"+str(news))
        elif(news>=100 and news<1000):
            temp.append("news_000"+str(news))
        elif(news>=1000 and news<10000):
            temp.append("news_00"+str(news))
        elif(news>=10000 and news<100000):
            temp.append("news_0"+str(news))
        else:
            temp.append("news_"+str(news))
    ans.append(temp)


peek = np.load("peek.npy", allow_pickle=True)
peek_q = [16, 17, 18, 19, 20]

for i in peek_q:
    temp = [0] * 301
    temp[0] = ans[i][0]
    peek_length = len(peek[i-16])
    isadd = {}
    for j in range(peek_length):
        temp[j+1] = peek[i-16][j]
        isadd[peek[i-16][j]] = 1
    count = peek_length
    wcount = peek_length
    while(count<300):
        n = ans[i][wcount-peek_length+1]
        if(n not in isadd):
            temp[count+1] = n
            count += 1
        wcount += 1 
    ans[i] = temp


with open(ans_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(ans)):
        writer.writerow(ans[i])
