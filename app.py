import os
import socket

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from utils import get_chart_data, predict_next_day

DEFAULT_PORT = 5555
DEFAULT_HOST = "127.0.0.1"


app = Flask(__name__)
CORS(app)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chart")
def chart():
    try:
        return jsonify(get_chart_data())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/predict")
def predict():
    try:
        return jsonify(predict_next_day())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if os.environ.get("PORT") and os.environ.get("FLASK_DEBUG") != "1":
    get_chart_data()


def find_free_port(start=DEFAULT_PORT, attempts=20):
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found between {start} and {start + attempts - 1}")


if __name__ == "__main__":
    get_chart_data()
    host = os.environ.get("HOST", DEFAULT_HOST)
    preferred = int(os.environ.get("PORT", DEFAULT_PORT))
    port = find_free_port(preferred)
    if port != preferred:
        print(f"Port {preferred} is busy, using port {port} instead.")
    print(f"Open in browser: http://localhost:{port}")
    app.run(debug=True, host=host, port=port, use_reloader=False)
