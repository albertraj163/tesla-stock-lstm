# Tesla Stock Forecaster

LSTM model for Tesla stock price prediction with a web UI.

## Open App

### https://albertraj163.github.io/tesla-stock-lstm/

Enga irundhalum open pannunga — phone, laptop, office, vera server.

Current live tunnel: https://maintenance-justin-performer-rendered.trycloudflare.com

---

## Open App (Public Link)

Run this on your server:

```bash
chmod +x run_public.sh stop_server.sh status_server.sh run_server.sh
./run_public.sh
```

It prints a **trycloudflare.com** link — open it from anywhere (phone, office, another server).

```bash
./status_server.sh   # check if running + get public URL
./stop_server.sh     # stop server and tunnel
```

---

## Local Setup

```bash
pip install -r requirements.txt
python3 train_lstm.py    # train LSTM (auto-runs on first server start)
python3 app.py           # dev server on http://localhost:5555
```

## Project Files

| File | Description |
|------|-------------|
| `app.py` | Flask web app with chart + prediction API |
| `train_lstm.py` | Train and save LSTM model |
| `predict.py` | CLI next-day price prediction |
| `utils.py` | Shared data loading and model helpers |
| `tesla_stock_sample.csv` | Tesla daily close prices (auto-expanded via yfinance) |

GitHub Repo: https://github.com/albertraj163/tesla-stock-lstm
