import glob
import json
import pandas as pd
import re


def file_to_dataframe(file_path):
    data = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    print(file_path + ' loaded')
    return pd.DataFrame(data)


def join_files_to_dataframe(files):
    file_list = glob.glob(files + "/*.json")
    data = []
    for file in file_list:
        with open(file, encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    return pd.DataFrame(data)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())


def get_unique_tweets(dataframe):
    return dataframe.drop_duplicates(subset='id')


def sort_by(dataframe, sort_column):
    return dataframe.sort_values(by=sort_column, ascending=False)


def date_and_time(row):
    return row["date"] + " " + row["time"]
