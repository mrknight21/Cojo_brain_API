from nltk.tokenize import word_tokenize
from textblob import  TextBlob
from utility.text_preprocessing import clean_text
'''
Argument:
    text: a long string
    cleaned: indicating whether the text has been preprocessed or not
'''


class SimpleAnalyzer(object):
    WPM = 200

    def __init__(self, cleaned = False, bulk_text = None):
        self.bulk_text = bulk_text
        self.cleaned = cleaned
        if not cleaned:
            self.text = self.standard_text_preprocessing(self.text)
            self.cleaned = True

    def standard_text_preprocessing(self, text):
        return clean_text(text)





    def ananlyze(self):
        pass
        # if not self.bulk_text: return []
        # ananlyze()

def estimate_reading_time(text):
    text = clean_text(text)
    words  = word_tokenize(text)
    print(words)
    est_reading_ms = 200*len(words)
    return round(est_reading_ms/1000)

def tester():
    text = 'bryan is a bad boy. He is going to the states.'
    blob = TextBlob(text)
    tags = blob.tags
    print(tags)
    polarity = blob.sentiment[0]
    subjectivity = blob.sentiment[1]
    print('polarity score: {}'.format(polarity))
    print('subjectivity score: {}'.format(subjectivity))
    print("estimated reading time: {} s".format(estimate_reading_time(text)))

if __name__ == "__main__":
    tester()
