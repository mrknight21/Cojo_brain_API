import nltk
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



def tester():
    text = 'bryan is handsome boy'
    blob = TextBlob(text)
    tags = blob.tags
    print(tags)
    polarity = blob.sentiment[0]
    subjectivity = blob.sentiment[1]
    print('polarity score: {}'.format(polarity))
    print('subjectivity score: {}'.format(subjectivity))

if __name__ == "__main__":
    tester()
