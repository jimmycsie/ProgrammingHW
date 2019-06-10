import json as js
import jieba
import numpy as np
import csv
jieba.set_dictionary('dict.txt.big')

query_seg=[]
word_terms_freq = {}
word_to_index = {}
query = []
dictionary_size = 8000
document_num = 100000
query_path = "./news_data_1/QS_1.csv"
ans_path = "ans.csv"

def check(word):
    ignore = ['，', '。', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
              '-', '+', '=', '[', ']', ',', '.', '<', '>', '/', ';', ':', 
              '\'', '\"', '{', '}', '、', '\n','\r', '\t', '\a', '\b', '\f', '\v']
    for i in ignore:
        if(word == i):
            return False
    return True

with open('url2content.json') as f:
	texts = js.load(f)
with open('word_to_index.json') as f:
	word_to_index = js.load(f)
with open('word_terms_freq.json') as f:
	word_terms_freq = js.load(f)
news_bag = np.load("news_bag.npy")


with open(file = query_path, mode = 'r') as csvfile:
    rows = csv.reader(csvfile)
    first = True
    for row in rows:
        if(first == True):
            first = False
            continue
        query.append(row[1])
    csvfile.close()

for q in query:
    query_seg.append(list(jieba.cut(q,cut_all=False)))

query_seg[0]=["通姦", "刑罰", "除罪"]
query_seg[1]=["取消", "機車", "強制", "二段式", "左轉", "待轉"]
query_seg[2]=["博弈", "台灣", "合法化"]
query_seg[3]=["中華", "航空", "空服員", "罷工", "合理"]
query_seg[4]=["性交易", "合法化"]
query_seg[5]=["ECFA", "早收", "清單", "成效"]
query_seg[6]=["減免", "證所稅"]
query_seg[7]=["贊成", "中油", "觀塘", "天然氣", "接收站"]
query_seg[8]=["支持", "中國", "學生", "納入", "健保"]
query_seg[9]=["支持", "台灣", "中小學", "高職", "專科", "服儀", "髮", "襪", "鞋", "自主"]
query_seg[10]=["不支持", "不", "加密", "貨幣"]
query_seg[11]=["不支持", "不", "學雜費", "調漲"]
query_seg[12]=["同意", "政府", "舉債", "發展", "前瞻", "建設", "計畫"]
query_seg[13]=["支持", "電競", "列入", "體育", "競技"]
query_seg[14]=["反對", "台鐵", "東移", "徵收"]
query_seg[15]=["支持", "陳水扁","總統", "保外", "就醫"]
query_seg[16]=["年金", "改革", "取消", "調降", "軍公教", "月退", "優存", "利率", "十八"]
query_seg[17]=["同意", "動物", "實驗"]
query_seg[18]=["油價", "凍漲", "緩漲"]
query_seg[19]=["反對", "旺旺", "中時", "併購", "中嘉"]

print(word_terms_freq["通姦"], word_terms_freq["刑罰"], word_terms_freq["除罪"])
print(word_to_index["除罪"])


tf_idf_score = []
no_word=[]
for i in range(len(query_seg)):
    temp = []
    for k in range(document_num):
        score = 0
        for j in range(len(query_seg[i])):
            if(query_seg[i][j] in word_to_index):
                index = word_to_index[query_seg[i][j]]
                score += news_bag[k][index] * np.log10(document_num/word_terms_freq[query_seg[i][j]])
                if(score<0):
                    print("error:", score, word_terms_freq[query_seg[i][j]])

        temp.append( (score,k+1) )
    tf_idf_score.append(temp)
    print(i)



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
    for i in range(300):
        news = rank[i][1]
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

with open(ans_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(ans)):
        writer.writerow(ans[i])
