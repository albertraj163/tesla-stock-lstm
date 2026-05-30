"""Train the Tesla LSTM model and save artifacts."""

from utils import METRICS_PATH, MODEL_PATH, SCALER_PATH, train_and_save


def main():
    print("Loading Tesla stock data...")
    df, model, scaler, metrics = train_and_save()
    print(f"Trained on {len(df)} rows.")
    print(f"RMSE: ${metrics['rmse']:.2f}")
    print(f"MAE:  ${metrics['mae']:.2f}")
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved scaler to {SCALER_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")


if __name__ == "__main__":
    main()
