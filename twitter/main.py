from twitter.influencers_finder.top_influencers import find_influencers_in_tweets, find_influencers_in_stats, find_users_tweets_and_extract_sentiments
from twitter.data_downloader.scrapper import scrap_user
import os
import json


HASHTAG = "BTC"
DATA_DIR = ".\\data\\"
USER_STATS_FILE_PATH = DATA_DIR + HASHTAG + '\\users_stats.txt'


def get_user_stats(files, number):
     top_users = list(find_influencers_in_tweets(files, number)['username'])
     print(top_users)
     for idx in range(0, number):
         scrap_user(top_users[idx], USER_STATS_FILE_PATH)


def get_top_influencers(number):
    if os.path.exists(USER_STATS_FILE_PATH):
        top_influencers = []
        with open(DATA_DIR + HASHTAG + "\\influencers.txt", 'r') as f:
            for line in f:
                top_influencers.append(line.rstrip())
    else:
        top_influencers = find_influencers_in_stats(USER_STATS_FILE_PATH, number)['username']
        with open(DATA_DIR + HASHTAG + "\\influencers.txt", 'x') as f:
            for user in top_influencers:
                f.write(user + "\n")
    return top_influencers


def get_influencers_tweets(influencers):
    for influencer in influencers:
        influencers_tweets = find_users_tweets_and_extract_sentiments(DATA_DIR + HASHTAG, influencer)

        with open(DATA_DIR + HASHTAG + "\\influencers\\" + influencer + "_tweets.json", 'w') as f:
            json.dump(influencers_tweets, f)


get_user_stats(DATA_DIR + HASHTAG, 100)
influencers = get_top_influencers(10)
get_influencers_tweets(influencers)
