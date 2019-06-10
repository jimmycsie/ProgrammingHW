import json as js
import jieba
import numpy as np
jieba.set_dictionary('dict.txt.big')

news_seg=[]
word_to_freq = {}
word_terms_freq = {}
word_to_index = {}
specialization = ["二段式", "專科", "服儀", "襪", "緩漲"]
dictionary_size = 8000 - len(specialization)


def check(word):
    ignore = ['，', '。', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
              '-', '+', '=', '[', ']', ',', '.', '<', '>', '/', ';', ':', 
              '\'', '\"', '{', '}', '、', '\n','\r', '\t', '\a', '\b', '\f', '\v']
    for i in ignore:
        if(word == i):
            return False
    return True


jieba.initialize()
with open('url2content.json') as f:
	texts = js.load(f)

count = 0
for url in texts:
    news_seg.append(list(jieba.cut(texts[url],cut_all=False)))
    count += 1
    if(count%1000==0):
        print(count)



# making dictionary
for i in range(len(news_seg)):
    counted = {}
    for j in range(len(news_seg[i])):
        if(news_seg[i][j] not in counted):                  # every word counts once for every terms
            if(check(news_seg[i][j])==True):
                if(news_seg[i][j] not in word_terms_freq):
                    word_terms_freq[news_seg[i][j]] = 1
                else:
                    word_terms_freq[news_seg[i][j]] += 1
                counted[news_seg[i][j]] = 1
            
        if(check(news_seg[i][j])==True):                    # every word counts once for every observation
            if(news_seg[i][j] not in word_to_freq):
                word_to_freq[news_seg[i][j]] = 1
            else:
                word_to_freq[news_seg[i][j]] += 1

    if(i%1000==0):
        print(i)


count = 1
for key, value in sorted(word_to_freq.items(), key=lambda item: item[1], reverse=True):
    if(count == dictionary_size):
        break
    word_to_index[key] = count
    count += 1
        
for i in range(len(specialization)):
    word_to_index[specialization[i]] = dictionary_size+i+1


json = js.dumps(word_to_index)
f = open("word_to_index.json","w")
f.write(json)
f.close()


json = js.dumps(word_terms_freq)
f = open("word_terms_freq.json","w")
f.write(json)
f.close()



