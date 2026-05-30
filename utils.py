import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential, load_model

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "tesla_stock_sample.csv"
MODEL_PATH = BASE_DIR / "tesla_lstm_model.keras"
SCALER_PATH = BASE_DIR / "scaler.joblib"
METRICS_PATH = BASE_DIR / "metrics.json"

LOOK_BACK = 5
EPOCHS = 50
BATCH_SIZE = 8
LSTM_UNITS = 50


def fetch_tesla_data():
    import yfinance as yf

    ticker = yf.Ticker("TSLA")
    history = ticker.history(start="2019-01-01", auto_adjust=True)
    if history.empty:
        raise RuntimeError("Could not download Tesla stock data from Yahoo Finance.")

    df = history.reset_index()[["Date", "Close"]].copy()
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    df = df.sort_values("Date")
    return df


def load_data():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
        df = df.sort_values("Date")
        if len(df) >= LOOK_BACK + 10:
            return df

    df = fetch_tesla_data()
    df.to_csv(DATA_PATH, index=False)
    return df


def create_dataset(series, look_back=LOOK_BACK):
    x_values, y_values = [], []
    for index in range(len(series) - look_back):
        x_values.append(series[index : index + look_back])
        y_values.append(series[index + look_back])
    return np.array(x_values), np.array(y_values)


def build_model(look_back=LOOK_BACK):
    model = Sequential(
        [
            LSTM(LSTM_UNITS, input_shape=(look_back, 1)),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    return model


def train_and_save():
    import joblib

    df = load_data()
    values = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    values_scaled = scaler.fit_transform(values)

    x_train, y_train = create_dataset(values_scaled)
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))

    model = build_model()
    model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)

    predictions = model.predict(x_train, verbose=0)
    actual = scaler.inverse_transform(y_train.reshape(-1, 1)).flatten()
    predicted = scaler.inverse_transform(predictions).flatten()

    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
    mae = float(np.mean(np.abs(actual - predicted)))

    model.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    METRICS_PATH.write_text(
        json.dumps(
            {
                "rmse": round(rmse, 2),
                "mae": round(mae, 2),
                "epochs": EPOCHS,
                "look_back": LOOK_BACK,
                "samples": len(df),
            }
        )
    )

    return df, model, scaler, {"rmse": rmse, "mae": mae}


def load_artifacts():
    import joblib

    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        train_and_save()

    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    metrics = {}
    if METRICS_PATH.exists():
        metrics = json.loads(METRICS_PATH.read_text())
    return model, scaler, metrics


def get_chart_data():
    model, scaler, metrics = load_artifacts()
    df = load_data()
    values = df["Close"].values.reshape(-1, 1)
    values_scaled = scaler.transform(values)

    x_data, y_data = create_dataset(values_scaled)
    x_data = x_data.reshape((x_data.shape[0], x_data.shape[1], 1))
    predictions = model.predict(x_data, verbose=0)

    dates = df["Date"].iloc[LOOK_BACK:].dt.strftime("%Y-%m-%d").tolist()
    actual = scaler.inverse_transform(y_data.reshape(-1, 1)).flatten().tolist()
    predicted = scaler.inverse_transform(predictions).flatten().tolist()

    return {
        "dates": dates,
        "actual": [round(value, 2) for value in actual],
        "predicted": [round(value, 2) for value in predicted],
        "metrics": metrics,
        "latest_date": df["Date"].iloc[-1].strftime("%Y-%m-%d"),
        "latest_close": round(float(df["Close"].iloc[-1]), 2),
    }


def predict_next_day():
    model, scaler, metrics = load_artifacts()
    df = load_data()
    recent = df["Close"].tail(LOOK_BACK).values.reshape(-1, 1)
    recent_scaled = scaler.transform(recent)
    input_batch = recent_scaled.reshape(1, LOOK_BACK, 1)
    prediction_scaled = model.predict(input_batch, verbose=0)
    predicted_price = float(scaler.inverse_transform(prediction_scaled)[0][0])

    return {
        "predicted_price": round(predicted_price, 2),
        "based_on_dates": df["Date"].tail(LOOK_BACK).dt.strftime("%Y-%m-%d").tolist(),
        "based_on_prices": [round(float(price), 2) for price in recent.flatten()],
        "latest_close": round(float(df["Close"].iloc[-1]), 2),
        "latest_date": df["Date"].iloc[-1].strftime("%Y-%m-%d"),
        "metrics": metrics,
    }
