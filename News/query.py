import numpy as np
import json as js
import jieba
from gensim.models import word2vec

query_seg = [0] * 20
query_bag = []
document_num = 100000
with open('word_to_index.json') as f:
	word_to_index = js.load(f)
with open('word_terms_freq.json') as f:
	word_terms_freq = js.load(f)
model = word2vec.Word2Vec.load("word2vec.model")


query_seg[0]=["通姦", "通姦", "刑罰", "除罪"]
query_seg[1]=["取消", "機車", "強制", "二段式", "二段式", "左轉", "待轉"]
query_seg[2]=["博弈", "博弈", "台灣", "合法化"]         
query_seg[3]=["中華", "航空", "華航", "空服員", "罷工", "罷工", "合理"]         #加華航
query_seg[4]=["性交易","性交易", "合法化"]
query_seg[5]=["ECFA", "早收", "清單", "成效"]
query_seg[6]=["減免", "證所稅"]
query_seg[7]=["贊成", "中油", "觀塘", "天然氣", "天然氣", "接收站"]
query_seg[8]=["支持", "中國", "學生", "納入", "健保", "健保"]
query_seg[9]=["支持", "中小學", "高職", "專科", "服儀", "服儀", "自主"]
query_seg[10]=["不支持", "加密", "貨幣"]
query_seg[11]=["不支持", "學雜費", "學雜費", "調漲"]
query_seg[12]=["同意", "舉債", "發展", "前瞻","前瞻", "建設", "計畫"]       #刪政府
query_seg[13]=["支持", "電競", "電競", "列入", "體育", "競技"]
query_seg[14]=["反對", "台鐵", "南鐵", "南鐵", "東移", "徵收"]      #台鐵改兩個南鐵
query_seg[15]=["支持", "陳水扁", "陳水扁", "總統", "保外", "就醫", "阿扁", "特赦"]      #阿扁 特赦
query_seg[16]=["年金", "改革", "取消", "調降", "軍公教", "月退", "優存", "利率", "十八", "18%"]  #18%
query_seg[17]=["同意", "動物", "實驗"]
query_seg[18]=["油價","油價", "凍漲", "緩漲"]
query_seg[19]=["反對", "旺旺", "中時", "併購", "中嘉", "旺中"]  #旺中
#1 10 11 14 16 18 19


si = model.most_similar(positive=['通姦'], topn = 30)
print(si[0][0])

for x in si:
    print(x[0],x[1])
"""
# query bag----------------------------------------------------------------------------------------
dictionary_size = 8000
for i in range(len(query_seg)):
    temp = np.zeros((dictionary_size+1))
    for j in query_seg[i]:
        temp[word_to_index[j]] += 1
    query_bag.append(temp)

query_bag = np.reshape(query_bag, (len(query_seg), dictionary_size+1))
for i in range(len(query_bag)):
    query_bag[i][0] = query_bag[i].sum()

for i in range(len(query_seg)):
    for j in query_seg[i]:
        if(j in word_terms_freq):
            query_bag[i][word_to_index[j]] = query_bag[i][word_to_index[j]]*np.power(np.log10(document_num/word_terms_freq[j]), 1.9) / query_bag[i][0]
        else:
            query_bag[i][word_to_index[j]] = query_bag[i][word_to_index[j]]*np.power(np.log10(document_num), 1.9) / query_bag[i][0]

print(query_bag.shape)
np.save("query_bag.npy", query_bag)


# query vec----------------------------------------------------------------------------------------
dictionary_size = 200
query_vec = []
for i in range(len(query_seg)):
    temp = [0]*dictionary_size
    for j in query_seg[i]:
        if(j in word_terms_freq):
            temp += model.wv[j]*np.power(np.log10(document_num/word_terms_freq[j]), 0.9) / len(query_seg[i])    
        else:
            temp += model.wv[j]*np.power(np.log10(document_num), 0.9) / len(query_seg[i])          
        if(j not in model.wv):
            print(j)
    query_vec.append(temp)

query_vec = np.array(query_vec)
np.save("query_vec.npy", query_vec)



# News vec----------------------------------------------------------------------------------------
news_seg = []
news_vec = []


jieba.load_userdict('dict.txt.big')
jieba.suggest_freq("ECFA", True)
jieba.suggest_freq("十八", True)
jieba.suggest_freq("陳水扁", True)
jieba.suggest_freq("通姦", True)
jieba.suggest_freq("二段式", True)
jieba.suggest_freq("待轉", True)
jieba.suggest_freq("空服員", True)
jieba.suggest_freq("性交易", True)
jieba.suggest_freq("服儀", True)
jieba.suggest_freq("不支持", True)
jieba.suggest_freq("加密", True)
jieba.suggest_freq("東移", True)
jieba.suggest_freq("月退", True)
with open('url2content.json') as f:
	texts = js.load(f)

count = 0
for url in texts:
    news_seg = list(jieba.cut(texts[url],cut_all=False))
    temp = [0]*dictionary_size
    for i in news_seg:
        if(i in model.wv and i in word_terms_freq):
            temp += model.wv[i]*np.power(np.log10(document_num/word_terms_freq[i]), 1.1) / len(news_seg)    
    news_vec.append(temp)
    count += 1
    if(count%10000==0):
        print(count)


news_vec = np.array(news_vec)
np.save("news_vec.npy", news_vec)
"""