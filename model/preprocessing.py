import numpy as np


# look_back - the number of previous time steps to use as input variables to predict the next time period
def get_sentiments_prices(sentiments1, sentiments2, prices, look_back=1):
    x, y = [], []
    for i in range(len(sentiments1) - look_back):
        x.append([sentiments1[i], sentiments2[i], prices[i]])
        y.append(prices[i + look_back])
    return np.array(x), np.array(y)


def normalize_array(array):
    normalized = (array - min(array)) / (max(array) - min(array))
    return normalized


def split(x):
    train_size = int(len(x) * 0.8)
    train = x[0:train_size]
    test = x[train_size:]
    return train, test


