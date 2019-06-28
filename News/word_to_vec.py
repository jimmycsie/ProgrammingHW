import json as js
import numpy as np
import jieba
from gensim.models.word2vec import Word2Vec

news_seg = []
with open('url2content.json') as f:
	texts = js.load(f)

jieba.load_userdict('dict.txt.big')
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

count = 0
for url in texts:
    news_seg.append(list(jieba.cut(texts[url],cut_all=False)))
    count += 1
    if(count%10000==0):
        print(count)
"""
for i in range(len(news_seg)):
    for j in range(len(news_seg[i])):
        if(news_seg[i][j]=="二段式" or news_seg[i][j]=="通姦"):
            print(news_seg[i][j])
"""

WordVec = Word2Vec(news_seg,min_count = 5, iter=5, workers=4, size=200, sg = 1)
WordVec.save("wordToVec200.model")


