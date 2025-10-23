import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

DATA_PATH = 'tesla_stock_sample.csv'

def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
    df = df.sort_values('Date')
    return df

def create_dataset(series, look_back=5):
    X, y = [], []
    for i in range(len(series) - look_back):
        X.append(series[i:(i+look_back)])
        y.append(series[i+look_back])
    return np.array(X), np.array(y)

def main():
    df = load_data()
    values = df['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    values_scaled = scaler.fit_transform(values)

    look_back = 5
    X, y = create_dataset(values_scaled, look_back)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential([LSTM(50, input_shape=(look_back, 1)), Dense(1)])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=50, batch_size=8, verbose=0)

    plt.plot(df['Date'][look_back:], scaler.inverse_transform(y.reshape(-1,1)), label='Actual')
    preds = model.predict(X)
    plt.plot(df['Date'][look_back:], scaler.inverse_transform(preds), label='Predicted')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
