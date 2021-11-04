import os
import pandas as pd
import random
from spacy.util import minibatch
import spacy
from spacy.pipeline.textcat import DEFAULT_SINGLE_TEXTCAT_MODEL
from spacy.training import Example
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

negative_train = 'D:/qiongyun/desktop/Master/nlp_chatbot/lab5/aclImdb/train/neg'
postive_train = 'D:/qiongyun/desktop/Master/nlp_chatbot/lab5/aclImdb/train/pos'
filesn = os.listdir(negative_train)
filesp = os.listdir(postive_train)
s = []

# ===================== 資料前處理 ====================================#

# 讀取資料夾內的檔案並給與 label -> [label, text]
for idx, file in enumerate(filesn):
    # f = open(negative_train+"/"+file)
    with open(negative_train+"/"+file,'r',encoding = 'utf8') as f:
        s.append(['neg', f.readline()])

for idx, file in enumerate(filesp):
    with open(postive_train+"/"+file,'r',encoding = 'utf8') as f:
        s.append(['pos', f.readline()])

# 命名 DataFrame column 名稱
columname = ['label','text']
data = pd.DataFrame(s, columns=columname)


train_texts = data['text'].values
#將文本和label連結
train_labels = [{'cats': {'neg': label == 'neg',
                          'pos': label == 'pos'}} for label in data['label']]
train_data = list(zip(train_texts, train_labels))


# Create an empty model and we will add pipe to it
nlp = spacy.blank("en") #新增空的NLP框架
#設定模型，這邊選用spaCy中預設的 text classfication 模型架構
config = {
   "threshold": 0.5,
   "model": DEFAULT_SINGLE_TEXTCAT_MODEL,
}
#將Text classfication 模型加入NLP框架中
textcat = nlp.add_pipe("textcat", config=config)
#設定需要辨識的label
textcat.add_label("neg")
textcat.add_label("pos")


# ========================= 訓練模型 =================================#

optimizer = nlp.begin_training()

for epoch in range(5):
    losses = {}
    random.shuffle(train_data)
    batches = minibatch(train_data, size=10) # Create the batch generator with batch size = 8

    for batch in batches:                   # Iterate through minibatches
        texts, labels = zip(*batch)         # use zip and unpack text, label for next line to update

        example = []
        for i in range(len(texts)):
            doc = nlp.make_doc(texts[i])
            #print(doc.text, labels[i])
            example.append(Example.from_dict(doc, labels[i]))
        nlp.update(example, sgd=optimizer, losses=losses)
    nlp.update(example, drop=0.5, losses=losses)
    # print(losses)

# ============================== Predictions==============================#

# Last Night in Soho reviews 5 pos and 5 neg
text = [
    "His riff on pulp Giallo thrillers from the sixties and seventies lack the bad taste that made them so celebrated.",
    "Wright's screenplay has a third act problem, where the revealing of the whats-and-hows aren't as interesting being lost in the whys.",
    "Unfortunately, as is too often the case with promising horror films, this one devolves into a disappointing mess toward the end.",
    "Edgar Wright is back to give us a weird and fun thriller with a touch of magic but, in the end, throws it for a bad loop with too much of a twist.",
    "The problem is that there's very little respite, and as the film becomes wearing, it also loses its potential to be genuinely disturbing.",
    "Last Night In Soho is a grand and gorgeous mess in the name of ambition.",
    "I love when horror is approached creatively like this, when it's gorgeous and seductive, and a little bit crazy!",
    "The most stylish and upscale horror movie in years.",
    "The movie is alive, intoxicated on life-possibilities and suffering over the extent of evil. It's bursting with color and fabric, songs and dances, ghosts and history.",
    "Horrible ending but the rest is excellent! Taylor-Joy & McKenzie are both great leading ladies. Another fantastic homage to the Giallo horror genre from Italy after Malignant."
]

# 字轉成向量
docs = [nlp.tokenizer(text) for text in texts]
# Use textcat to get the scores for each doc
textcat = nlp.get_pipe('textcat')
scores = textcat.predict(docs)
print(scores)

# From the scores, find the label with the highest score/probability
predicted_labels = scores.argmax(axis=1)
print([textcat.labels[label] for label in predicted_labels])