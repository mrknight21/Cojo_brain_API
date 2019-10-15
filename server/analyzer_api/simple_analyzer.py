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

    def __init__(self,  bulk_text, cleaned = False,):
        self.bulk_text = bulk_text
        self.cleaned = cleaned
        if not self.cleaned:
            self.bulk_text = self.standard_text_preprocessing(self.bulk_text)
            self.cleaned = True

    def standard_text_preprocessing(self, bulk_text):
        return list(map(lambda x: clean_text(x) ,bulk_text))

    def single_ananlyze(self, text):
        polarity_scores = []
        subjectivity_scores = []
        reading_time = self.estimate_reading_time(text)
        blob = TextBlob(text)
        for sent in blob.sentences:
            polarity_scores.append(sent.sentiment.polarity)
            subjectivity_scores.append(sent.sentiment.subjectivity)
        p_avg = np.mean(polarity_scores)
        s_avg = np.mean(subjectivity_scores)
        return p_avg, s_avg, reading_time

    def bulk_analyze(self):
        if not self.cleaned:
            self.bulk_text = self.standard_text_preprocessing(self.text)
            self.cleaned = True
        return [(self.single_ananlyze(text)) for text in self.bulk_text]

    def estimate_reading_time(self, text):
        text = clean_text(text)
        words = word_tokenize(text)
        est_reading_ms = 200*len(words)
        return round(est_reading_ms/1000)

def tester():
    text = ['bryan is a bad boy. He is going to the states.', 'Jamse is coming back to NZ. And jojo is gonna start a party']
    analyzer = SimpleAnalyzer(text)
    print(analyzer.bulk_analyze())

if __name__ == "__main__":
    tester()
