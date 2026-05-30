"""CLI helper for next-day Tesla price prediction."""

import argparse

from utils import predict_next_day


def main():
    parser = argparse.ArgumentParser(description="Predict next Tesla stock close price")
    parser.parse_args()

    result = predict_next_day()
    print(f"Latest close ({result['latest_date']}): ${result['latest_close']:.2f}")
    print(f"Predicted next close: ${result['predicted_price']:.2f}")
    print(f"Based on last {len(result['based_on_prices'])} days:")
    for day, price in zip(result["based_on_dates"], result["based_on_prices"]):
        print(f"  {day}: ${price:.2f}")


if __name__ == "__main__":
    main()
