from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import math


def get_avg_sentiments(sentences):
    if len(sentences) == 0:
        return 0
    return np.mean(analyze_sentiments(sentences))


def analyze_sentiments(sentences):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = [0 if str(s) == 'nan' else analyzer.polarity_scores(s)['compound'] for s in sentences]
    return sentiments


def analyze_sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(sentence)['compound']
