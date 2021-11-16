# Chatbot_NLP 
### Lab 4  
Lab 4 是利用 Word embedding 的方式，將詞轉換為 vectors 的形式，透過相近的字會聚在一起的特性，來計算出在空間中距離的遠近得出其相似的程度。但此方法會有一些詬病，因為有些 word 會有多個含意，必須由上下文判斷，如果只是用一個 vector 來表示語意的話會無法 fit 每一個狀況。因此就會有以下狀況，像是在[7,0]中[0,7]今天買了蘋果手機 會有被辨識成蘋果(水果)機率比較高的情形。

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
