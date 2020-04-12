from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import  TextBlob
from utility.text_preprocessing import clean_text
import numpy as np
'''
Argument:
    text: a long string
    cleaned: indicating whether the text has been preprocessed or not
'''


class SimpleAnalyzer(object):
    WPM = 200

    def __init__(self,  cleaned = False,):
        # self.bulk_text = bulk_text
        self.cleaned = cleaned
        # if not self.cleaned:
        #     self.bulk_text = self.standard_text_preprocessing(self.bulk_text)
        #     self.cleaned = True

    def single_text_preprocessing(self, text):
        text = clean_text(text)
        return text

    def bulk_text_preprocessing(self, bulk_text):
        return list(map(lambda x: clean_text(x) ,bulk_text))

    def single_analyze(self, text):
        text = self.single_text_preprocessing(text)
        insight = {'polarity':0.0, 'subjectivity': 0.0, 'reading_time': 0, 'words_count':0}
        insight['polarity'], insight['subjectivity'] = self.text_blob_scoring(text)
        insight['reading_time'], insight['words_count'] = self.estimate_reading_time(text)
        return insight

    def text_blob_scoring(self, text):
        polarity_scores = []
        subjectivity_scores = []

        blob = TextBlob(text)
        for sent in blob.sentences:
            polarity_scores.append(sent.sentiment.polarity)
            subjectivity_scores.append(sent.sentiment.subjectivity)
        p_avg = round(np.mean(polarity_scores), 2)
        s_avg = round(np.mean(subjectivity_scores), 2)
        return p_avg, s_avg


    def estimate_reading_time(self, text):
        text = clean_text(text)
        words = word_tokenize(text)
        est_reading_ms = 200*len(words)
        return round(est_reading_ms/1000), len(words)
def tester():
    text = 'bryan is a bad boy. He is going to the states. Jamse is coming back to NZ. And jojo is gonna start a party'
    analyzer = SimpleAnalyzer()
    print(analyzer.single_analyze(text))

if __name__ == "__main__":
    tester()
