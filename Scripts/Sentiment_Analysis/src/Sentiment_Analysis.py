import sys
import os
import time
import json
from collections import Counter
import nltk


class Sentiment_Analysizer:
    '''
    Uses classifier to determine a text's sentiment
    '''

    def __init__(self):
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()

        except LookupError:
            nltk.download('vader_lexicon')
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def determine_sentiment(self, text):
        '''
        Uses the VADER classifier to determine the sentiment of a give phrase or
        sentence

        params:
            text: str // A sentence or phrase
        '''
        pscores = self.sentiment_analyzer.polarity_scores(text)
        return pscores


def write_file(filename, obj):
    '''
    Writes an object to a specified file

    params:
        filename: str
        obj: object
    '''
    if filename[-4:] == 'json':
        with open(f'{filename}.json', 'w') as f:
            json.dump(obj, f)

    else:
        with open(filename, 'w') as f:
            f.write(obj)


def main():
    text = "I hate you"
    
    sent_analysizer = Sentiment_Analysizer()
    pscore = sent_analysizer.determine_sentiment(text)
    print(pscore)

if __name__ == "__main__":
    main()