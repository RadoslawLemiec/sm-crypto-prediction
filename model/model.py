from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import mean_squared_error
import keras
import tensorflow
import math


def create_model(hidden_size, look_forward, dropout):
    model = Sequential()
    model.add(LSTM(hidden_size, return_sequences=True, input_shape=(look_forward, 3)))
    model.add(Dropout(dropout))
    model.add(Dense(1))
    return model


def train(model, train_x, train_y, batch_size, epochs):
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x=train_x, y=train_y, epochs=epochs, batch_size=batch_size)
    return model


def test(model, test_x):
    y_pred = model.predict(test_x)
    return y_pred


def evaluate(y_true, y_pred):
    score = math.sqrt(mean_squared_error(y_true, y_pred))
    return score






