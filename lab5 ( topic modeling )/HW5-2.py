from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessing
from sklearn.datasets import fetch_20newsgroups
import nltk
from nltk.corpus import stopwords
import pyLDAvis
import pyLDAvis
import re
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
# spacy for lemmatization
import spacy


#  資料抓取 Import Newsgroups Data
newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
newsgroups_test = fetch_20newsgroups(subset='test', shuffle = True)


# NLTK Stop words (另外新增)
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

# 資料前處理 - Remove emails and newline characters

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Tokenize and lemmatize
def preprocess(text):
    # Convert to list
    # text = text.content.values.tolist()
    # Remove Emails
    text = [re.sub('\S*@\S*\s?', '', sent) for sent in text]
    # Remove new line characters
    text = [re.sub('\s+', ' ', sent) for sent in text]
    # Remove distracting single quotes
    text = [re.sub("\'", "", sent) for sent in text]
    return text


'''
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))

    return result
'''

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


processed_docs = []
for doc in newsgroups_train.data:
    processed_docs.append(preprocess(doc))

data_words = list(sent_to_words(processed_docs))


 # Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
sp = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()

tp = TopicModelDataPreparation("paraphrase-distilroberta-base-v1")

training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)


tp.vocab[:10]