import pandas as pd


def load_reddit_data(data_path):
    df = pd.read_csv(data_path, header=0, index_col=0)
    df["timestamp"] = df.timestamp.astype(int)
    return df
