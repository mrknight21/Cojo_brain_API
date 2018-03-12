import spacy
import pickle
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from os import listdir

class SimpleBayesian:
    """
    Usage:
    document = some string
    a = SimpleBayesian()
    a.predict(document)
    """
    def __init__(self, model_path='simpleNaiveBaysian.pickle'):
        f = open(model_path, 'rb')
        self.classifier, self.word_features = pickle.load(f)
        f.close()

    def predict(self, document):
        tokens = word_tokenize(document) # tokenise document
        feature_set = self.document_features(tokens) # determine which word features the document contains
        prediction = self.classifier.classify(feature_set) # make a prediction
        return prediction

    def document_features(self, doc):
        doc_words = set(doc)
        features = {}
        for word in self.word_features:
            features['contains({})'.format(word)] = (word in doc_words)
        return features

    def train_new(self, filepath, num_word_features=2000, test_split=0.8, new_name='simpleNaiveBaysian'):
        """
        Trains and saves new model with given parameters, using data available in provided path. 'filepath' must point at a folder that contains multiple
        folders; one for each class to classify. Each class folder must contain .txt files of documents to train on.
        :param filepath: the path to the folders containing the training examples
        :param num_word_features: Number of word features to base classification on; default is 2000.
        :param test_split: training/testing split. Default is 0.8, i.e. 80% of data used for training, the other 20% are used for testing.
        :param new_name: name under which to store new model. The default option is to overwrite the current model.
        :return:
        """
        textsets = []  # stores (text - class) pairs
        tokenset = []  # stores individual tokens across whole dataset
        for itemClass in listdir(filepath):
            if not '.' in itemClass: # only access folders
                print(itemClass)
                for item in listdir(filepath + '/' + itemClass):
                    with open(filepath + '/' + itemClass + '/' + item) as f:
                        txt = f.read()
                    txtTokens = word_tokenize(txt)
                    textsets.append((txtTokens, itemClass))
                    tokenset += txtTokens
        np.random.seed(1)
        np.random.shuffle(textsets)
        print("{} documents, total of {} word tokens collected.".format(len(textsets), len(tokenset)))

        tokenset = [w.lower() for w in tokenset]
        all_words = nltk.FreqDist(tokenset) # determines frequency distribution on words
        self.word_features = list(all_words)[:num_word_features]  # top N most unusual/uncommon words

        featuresets = [(self.document_features(d), c) for (d, c) in textsets]

        int_split = int(test_split * len(textsets))
        train_set, test_set = featuresets[:int_split], featuresets[int_split:]
        self.classifier = nltk.NaiveBayesClassifier.train(train_set) # new classifier generated
        print("{} split: {}".format(test_split, nltk.classify.accuracy(self.classifier, test_set)))

        f = open(new_name + '.pickle', 'wb')
        pickle.dump((self.classifier, self.word_features), f)
        f.close()
        print("New classifier stored under '{}'".format(new_name + '.pickle'))