from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import numpy as np
import pickle
from os import listdir

class MultinomialBayesian:
    def __init__(self):
        # Initialize tokenizer
        self.regexp_tokenizer = RegexpTokenizer('[\'a-zA-Z]+')

        # Load stop-words
        self.stop_words = set(stopwords.words('english'))

        # Initialize lemmatizer
        self.wordnet_lemmatizer = WordNetLemmatizer()

        f = open('multinomialNaiveBaysian.pickle', 'rb')
        self.model = pickle.load(f)
        f.close()

    def tokenize(self, document, rebuild_document=True):
        words = []

        for sentence in sent_tokenize(document):
            tokens = [self.wordnet_lemmatizer.lemmatize(t.lower())
                      for t in self.regexp_tokenizer.tokenize(sentence) if t.lower() not in self.stop_words]
            words += tokens

        if rebuild_document:
            return ' '.join(words).strip()
        else:
            return words

    def get_prediction(self, in_text):
        in_tokens = self.tokenize(in_text)
        prediction = self.category_reference[self.model.predict(in_tokens)[0]]
        return prediction
