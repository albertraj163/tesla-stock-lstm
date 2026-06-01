#!/usr/bin/env bash
# Run app in background on localhost

cd "$(dirname "$0")"
source "$(dirname "$0")/server_env.sh"

if [ ! -f "tesla_lstm_model.keras" ]; then
  echo "Training LSTM model (first time only)..."
  python3 train_lstm.py
fi

pkill -f "gunicorn app:app" 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 1

echo "Starting server on $APP_URL"
nohup gunicorn app:app \
  --bind "$HOST:$PORT" \
  --workers 1 \
  --timeout 300 \
  --daemon \
  --access-logfile access.log \
  --error-logfile error.log

echo "$APP_URL" > local_url.txt

echo ""
echo "  Server running!"
echo "  Open: $APP_URL"
echo ""
echo "  Stop:    ./stop_server.sh"
echo "  Status:  ./status_server.sh"
echo ""
