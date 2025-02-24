import threading
import time
from collections import deque
from datetime import datetime
from typing import Optional

import requests
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Bitcoin API URL
BITCOIN_API_URL: str = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# Store the last 10 prices
last_10_prices: deque[float] = deque(maxlen=10)


def fetch_bitcoin_price() -> Optional[float]:
    """Fetch Bitcoin price from the API."""
    try:
        response: requests.Response = requests.get(BITCOIN_API_URL)
        if response.status_code == 200:
            data: dict = response.json()
            return float(data['bitcoin']['usd'])
        else:
            print(f"Error fetching data: HTTP Status Code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None


def bitcoin_price_fetcher() -> None:
    """Background thread for fetching Bitcoin price."""
    i: int = 0
    while True:
        i += 1
        price: Optional[float] = fetch_bitcoin_price()
        time_val: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time_val)

        if price is not None:
            last_10_prices.append(price)
            print(f"Current Bitcoin price: ${price:.2f}")

            if i == 10:
                i = 0
                avg_price: float = sum(last_10_prices) / len(last_10_prices)
                print(f"Average Bitcoin price over the last 10 minutes: ${avg_price:.2f}")

        print()
        time.sleep(60)


@app.route("/healthz")
def healthz() -> tuple[str, int]:
    return "OK", 200


@app.route("/readiness")
def readiness() -> tuple[str, int]:
    return "OK", 200


if __name__ == "__main__":
    fetcher_thread: threading.Thread = threading.Thread(target=bitcoin_price_fetcher, daemon=True)
    fetcher_thread.start()

    app.run(host="0.0.0.0", port=8080)
