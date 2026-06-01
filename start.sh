#!/usr/bin/env bash
# Start app on localhost (foreground — for development)

cd "$(dirname "$0")"
source "$(dirname "$0")/server_env.sh"

if [ ! -f "tesla_lstm_model.keras" ]; then
  echo "Training LSTM model (first time only)..."
  python3 train_lstm.py
fi

echo "Starting Tesla Stock Forecaster on $APP_URL"
python3 app.py
