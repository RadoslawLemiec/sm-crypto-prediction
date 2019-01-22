import pandas as pd
import json
from twitter.data_preprocessing.preprocessing import get_unique_tweets


def load_tweets(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        json_file = json.load(data_file)
        df = pd.DataFrame(json_file)
    return get_unique_tweets(df)


def load_sentiment_time_data(file_path):
    df = pd.read_csv(file_path, header=0, index_col=0)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df
