# Tesla Stock Forecaster

LSTM model for Tesla stock price prediction with a web UI.

## Open App (Localhost)

**http://localhost:5555**

---

## Quick Start

```bash
pip install -r requirements.txt
chmod +x start.sh run_server.sh stop_server.sh status_server.sh
./run_server.sh
```

Open in browser: **http://localhost:5555**

```bash
./status_server.sh   # check if running
./stop_server.sh     # stop server
./start.sh           # run in foreground (dev mode)
```

---

## Train Model

```bash
python3 train_lstm.py
python3 predict.py    # CLI next-day prediction
```

## Project Files

| File | Description |
|------|-------------|
| `app.py` | Flask web app with chart + prediction API |
| `train_lstm.py` | Train and save LSTM model |
| `predict.py` | CLI next-day price prediction |
| `utils.py` | Shared data loading and model helpers |
| `server_env.sh` | Port and localhost URL config |
| `tesla_stock_sample.csv` | Tesla daily close prices |

**Port:** `5555`  
**Host:** `127.0.0.1` (localhost only)

GitHub Repo: https://github.com/albertraj163/tesla-stock-lstm
