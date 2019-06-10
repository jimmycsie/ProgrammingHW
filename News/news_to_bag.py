import json as js
import jieba
import numpy as np
jieba.set_dictionary('dict.txt.big')

dictionary_size = 8000
news_bag = []

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
    if(count%1000==0):
        print(count)

news_bag = np.array(news_bag)
print(news_bag.shape)
np.save("news_bag", news_bag)
