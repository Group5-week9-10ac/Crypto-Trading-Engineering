import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(data):
    """ Preprocess data: normalize using MinMaxScaler """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return scaler, scaled_data

def create_sequences(data, sequence_length):
    """ Create sequences for LSTM training """
    X = []
    y = []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length])
    return np.array(X), np.array(y)

def inverse_transform(scaler, data):
    """ Inverse transform data using given scaler """
    return scaler.inverse_transform(data)
