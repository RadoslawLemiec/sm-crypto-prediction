from datetime import datetime, timedelta
from sentiment_analyzer import get_avg_sentiments
import pandas as pd
import numpy as np


def create_dataset(df_coin, df_twitter, df_reddit, window_width, filename):
    dataset = pd.DataFrame(columns=["twitter_sentiments", "reddit_sentiments", "coin_price", "datetime"])
    df_coin["datetime"] = pd.to_datetime(df_coin["Date"])
    df_twitter["datetime"] = [datetime.strptime(row["date"] + " " + row["time"], "%Y-%m-%d %H:%M:%S") for _, row in df_twitter.iterrows()]
    df_reddit["datetime"] = pd.to_datetime(df_reddit["timestamp"], unit='s')

    df_coin = sort_by_date(df_coin)
    df_twitter = sort_by_date(df_twitter)
    df_reddit = sort_by_date(df_reddit)

    coin_idx, twitter_idx, reddit_idx, window_start = find_start_date_idxs(df_coin, df_twitter, df_reddit)
    window_time = timedelta(minutes=window_width)

    while coin_idx < len(df_coin) and twitter_idx < len(df_twitter) and reddit_idx < len(df_reddit):
        print(window_start)
        tweets = []
        reddits = []
        coins_prices = []

        while coin_idx < len(df_coin) and df_coin["datetime"].iloc[coin_idx] <= window_start + window_time:
            coins_prices.append(np.mean([df_coin["Open"].iloc[coin_idx], df_coin["Close"].iloc[coin_idx]]))
            coin_idx += 1

        while twitter_idx < len(df_twitter) and df_twitter["datetime"].iloc[twitter_idx] <= window_start + window_time:
            tweets.append(df_twitter["tweet"].iloc[twitter_idx])
            twitter_idx += 1

        while reddit_idx < len(df_reddit) and df_reddit["datetime"].iloc[reddit_idx] <= window_start + window_time:
            reddits.append(df_reddit["text"].iloc[reddit_idx])
            reddit_idx += 1

        coins_prices_avg = np.mean(coins_prices)
        tweets_sentiment_avg = get_avg_sentiments(tweets)
        reddits_sentiment_avg = get_avg_sentiments(reddits)

        dataset.loc[len(dataset)] = [tweets_sentiment_avg, reddits_sentiment_avg, coins_prices_avg, window_start]
        window_start += window_time

    dataset.to_csv(filename)
    print("Saved")
    print(dataset.head())
    return dataset


def find_start_date_idxs(df_coin, df_twitter, df_reddit):
    start_date_coins = df_coin["datetime"].iloc[0].replace(second=0)
    start_date_twitter = df_twitter["datetime"].iloc[0].replace(second=0)
    start_date_reddit = df_reddit["datetime"].iloc[0].replace(second=0)

    coin_idx = 0
    twitter_idx = 0
    reddit_idx = 0

    if max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_coins:
        start_date = start_date_coins
        while df_twitter["datetime"].iloc[twitter_idx] < start_date_coins:
            twitter_idx += 1
        while df_reddit["datetime"].iloc[reddit_idx] < start_date_coins:
            reddit_idx += 1

    elif max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_twitter:
        start_date = start_date_twitter
        while df_coin["datetime"].iloc[coin_idx] < start_date_twitter:
            coin_idx += 1
        while df_reddit["datetime"].iloc[reddit_idx] < start_date_twitter:
            reddit_idx += 1

    elif max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_reddit:
        start_date = start_date_reddit
        while df_coin["datetime"].iloc[coin_idx] < start_date_reddit:
            coin_idx += 1
        while df_twitter["datetime"].iloc[twitter_idx] < start_date_reddit:
            twitter_idx += 1

    return coin_idx, twitter_idx, reddit_idx, start_date


def sort_by_date(df):
    return df.sort_values(by='datetime')
