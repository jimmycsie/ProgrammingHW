import json as js
import jieba
import numpy as np

jieba.initialize()
jieba.set_dictionary('dict.txt.big')

news_seg=[]
word_to_freq = {}
word_terms_freq = {}
word_to_index = {}
news_bag = []
specialization = ["二段式", "專科", "服儀", "襪", "緩漲", "刑罰", "月退"]

# 同義詞
synonym = []
synonym.append( ["同意", "贊同", "支持", "認同", "過半", "贊成"] )      
synonym.append( ["不同意", "不贊同", "不支持", "不認同", "不贊成", "反對", "抵制", "批判"] )
synonym.append( ["合法", "合法化", "除罪", "除罪化", "合憲", "合於", "予以", "依法"] )
synonym.append( ["減免", "廢除", "停止", "中止", "停徵"] )      
#減免、廢除、停止、中止、停徵

#加強斷詞
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
jieba.suggest_freq("不贊成", True)
jieba.suggest_freq("不同意", True)
jieba.suggest_freq("不贊同", True)
jieba.suggest_freq("不認同", True)
jieba.suggest_freq("加密", True)
jieba.suggest_freq("東移", True)
jieba.suggest_freq("月退", True)

dictionary_size = 8000 - len(specialization)


def check(word):
    ignore = ['，', '。', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
              '-', '+', '=', '[', ']', ',', '.', '<', '>', '/', ';', ':', 
              '\'', '\"', '{', '}', '、', '\n','\r', '\t', '\a', '\b', '\f', '\v']
    for i in ignore:
        if(word == i):
            return False
    return True

def combine(word):
    for i in range(len(synonym)):
        if(word in synonym[i]):
            return synonym[i][0]
    return word



with open('url2content.json') as f:
	texts = js.load(f)

count = 0
for url in texts:
    news_seg.append(list(jieba.cut(texts[url],cut_all=False)))
    count += 1
    if(count%10000==0):
        print("(1/3)", count)


# making dictionary
for i in range(len(news_seg)):
    counted = {}
    for j in range(len(news_seg[i])):
        word = combine(news_seg[i][j])
        if(word not in counted):                  # every word counts once for every terms
            if(check(word)==True):
                if(word not in word_terms_freq):
                    word_terms_freq[word] = 1
                else:
                    word_terms_freq[word] += 1
                counted[word] = 1
            
        if(check(word)==True):                    # every word counts once for every observation
            if(word not in word_to_freq):
                word_to_freq[word] = 1
            else:
                word_to_freq[word] += 1

    if(i%10000==0):
        print("(2/3)", i)



count = 1
for key, value in sorted(word_to_freq.items(), key=lambda item: item[1], reverse=True):
    if(count == dictionary_size):
        break
    word_to_index[key] = count
    count += 1
        
for i in range(len(specialization)):
    word_to_index[specialization[i]] = dictionary_size+i+1


# 建立同義詞字典
for i in range(len(synonym)):
    for word in synonym[i]:
        if(combine(word) in word_to_index):
            word_to_index[word] = word_to_index[combine(word)]
            word_terms_freq[word] = word_terms_freq[combine(word)]



json = js.dumps(word_to_index)
f = open("word_to_index.json","w")
f.write(json)
f.close()


json = js.dumps(word_terms_freq)
f = open("word_terms_freq.json","w")
f.write(json)
f.close()

# news to bag ---------------------------------------------------------------
dictionary_size = 8000
count = 0
for url in texts:
    news_seg = list(jieba.cut(texts[url],cut_all=False))
    temp = np.zeros((dictionary_size+1))
    for j in news_seg:
        if(check(j)==True):
            if(j in word_to_index):
                temp[word_to_index[j]] += 1
    news_bag.append(temp)   
    count += 1
    if(count%10000==0):
        print("(3/3)", count)

news_bag = np.array(news_bag)
for i in range(news_bag.shape[0]):
    total_word = news_bag[i].sum()
    news_bag[i][0] = total_word

print(news_bag[0][0], news_bag[1][0])
print(news_bag.shape)
np.save("news_bag.npy", news_bag)

