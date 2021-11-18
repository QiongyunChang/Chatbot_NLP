[What is LaTeX?](#what-is-latex)



# Chatbot_NLP 
### Similarity matrix 

單純利用 Word embedding 的方式，將詞轉換為 vectors 的形式，透過相近的字會聚在一起的特性，來計算出在空間中距離的遠近得出其相似的程度。但此方法會有一些詬病，因為有些 word 會有多個含意，必須由上下文判斷，如果只是用一個 vector 來表示語意的話會無法 fit 每一個狀況。因此就會有以下狀況，像是在[7,0]中[0,7]今天買了蘋果手機 會有被辨識成蘋果(水果)機率比較高的情形。

![image](https://user-images.githubusercontent.com/51444652/141946507-6d965e2a-f82a-4985-9811-b0466c748df1.png)

### Lab 3

#### HW3-1 Entity Pairs & Relation Extraction
- 將句子中的**Entity Pairs**和**Relation**利用中文的Spacy模型找出來，舉例來說，如果題目是`我撐起那把雨傘`，輸出答案便是
###### Entity Pairs
```
['我', '雨傘']
```
###### Relation
```
撐起
``` 
- 找出下列句子中的**Entity Pairs**和**Relation**
    - `警察逮捕那個嫌犯` 
    - `我走進成功大學`
    - `他放棄了這堂課`
    
#### HW3-2 NER
請文本進行
- 分句
- Named Entity Recognition


#### HW3-3 Model Training 
- 經過直接inference可以發現，有一些entity是沒有抓出來的，所以我們會利用更新參數的方式來幫我們調整model到我們想要的狀態
- 讓model能夠辨識出`成功大學(ORG)`

### Lab 5
#### Sentiment analyze
* HW5-1.py 
  *   movie review sentiment analyze
  
#### Topic Modeling ( compare two method )
* LAB5_2.ipynb
  *  Topic Modeling - Contextualized Topic Models
  
* LDA.py
  *  Topic Modeling - LDA
  
* Dataset : fetch_20newsgroups
