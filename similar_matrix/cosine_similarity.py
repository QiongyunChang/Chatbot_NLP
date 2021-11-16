from sqlalchemy.sql import select
from sentence_transformers import SentenceTransformer, util
import spacy
from spacy.matcher import Matcher
import zh_core_web_lg
import scipy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column
import numpy as np
import spacy
nlp = spacy.load('zh_core_web_lg')
sentence = ["今天買了蘋果來吃","進口蘋果(富士)平均每公斤下跌12.3%","蘋果茶真難喝","老饕都知道智利的蘋果季節即將到來","進口蘋果因防止水燜流失故添加人工果蠟","蘋果即將於下月發布新款Iphone", "蘋果獲新 Face ID 專利", "今天買了蘋果手機","蘋果的股價又跌了","蘋果壓寶指紋辨識技術"]
# create 相似度矩陣
similar_ma = np.zeros(shape=(10,10))
n = 0
# 計算句子之間的相似程度
for i in sentence:
    search_doc = nlp(i)
    value = []
    for j in sentence:
        main_doc = nlp(j)
        # 提升準確率移除 stopword
        sentence_nostopw = nlp(' '.join([str(t) for t in search_doc if not t.is_stop]))
        target_nostopw = nlp(' '.join([str(t) for t in main_doc if not t.is_stop]))
        a= sentence_nostopw.similarity(target_nostopw)
        # 產生 row[i:] 的 list
        value.append(a)
    # print(value)
    # 形成 array
    similar_ma[n] = value
    n += 1
print(similar_ma)

#  10 * 10 相似度矩陣圖
import matplotlib.pyplot as plt
plt.imshow(similar_ma.reshape((10,10)))
plt.colorbar()
plt.show()
