from model.preprocessing import normalize_array, get_sentiments_prices, split
from model.model import create_model, train, test, evaluate
from main import create_dataset
from twitter.data_loader.loader import load_tweets
from crypto.data_loader.loader import load_crypto_data
from RedditWrapper.data_loader import load_reddit_data
import numpy as np
import pandas as pd


def load_social_datasets():
    df_twitter = load_tweets("..//twitter//data//tweets_all.json")
    df_reddit = load_reddit_data("..//RedditWrapper//prepared_reddit_data.csv")
    df_crypto = load_crypto_data("..//crypto//data//BTC-USD_2015-2018_1min")
    return df_crypto, df_twitter, df_reddit


def remove_nan(dataset, column_with_nan):
    nan_indexes = np.where(dataset[column_with_nan].isna())[0]
    indexes_sequences = []

    i = 0
    while i < len(nan_indexes) - 2:
        sequence = [nan_indexes[i]]
        j = i + 1

        while j < len(nan_indexes) and nan_indexes[j] - nan_indexes[j-1] == 1:
            sequence.append(nan_indexes[j])
            j += 1

        indexes_sequences.append(sequence)
        i = j

    for sequence in indexes_sequences:
        prev_not_nan_value = dataset[column_with_nan].iloc[sequence[0] - 1]
        next_not_nan_value = dataset[column_with_nan].iloc[sequence[-1] + 1]
        step = (next_not_nan_value - prev_not_nan_value) / (len(sequence) + 1)

        for i in range(len(sequence)):
            dataset[column_with_nan].iloc[sequence[i]] = dataset[column_with_nan].iloc[sequence[i] - 1] + step
    return dataset


def load_dataset(file_path):
    dataset = pd.read_csv(file_path, header=0, index_col=0)
    dataset = remove_nan(dataset, "coin_price")
    return dataset


def create_dataset(window_size, file_name):
    df_crypto, df_twitter, df_reddit = load_social_datasets()
    dataset = create_dataset(df_crypto, df_twitter, df_reddit, window_size, file_name)
    return dataset


def run_expreminent(look_forward, hidden_size, batch_size, epochs, dropout, dataset):
    x, y = get_sentiments_prices(dataset['twitter_sentiments'], dataset["reddit_sentiments"], dataset["coin_price"], look_forward)

    for i in range(x.shape[1]):
        x[:, i] = normalize_array(x[:, i])

    # split into train and test sets
    train_x, test_x = split(x)
    train_y, test_y = split(y)

    train_x = np.reshape(train_x, (train_x.shape[0], look_forward, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], look_forward, test_x.shape[1]))

    model = create_model(hidden_size=hidden_size, look_forward=look_forward, dropout=dropout)
    model = train(model, train_x, train_y, batch_size=batch_size, epochs=epochs)
    y_pred = test(model, test_x)
    score = evaluate(test_y, y_pred)
    print('Test Score: %.2f RMSE' % (score))
    return score


dataset = load_dataset("..//data//window-720.csv")
run_expreminent(look_forward=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2, dataset=dataset)
