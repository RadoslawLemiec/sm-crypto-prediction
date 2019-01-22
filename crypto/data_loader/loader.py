import pandas as pd
import glob


def load_crypto_data(file_path):
    files = glob.glob(file_path + "/*.csv")
    result = []

    for file in files:
        df = pd.read_csv(file, header=0)
        result.append(df)
    return pd.concat(result, axis=0)
