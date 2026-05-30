import os
import socket
from pathlib import Path

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from utils import get_chart_data, predict_next_day

DEFAULT_PORT = 5555


def get_server_ip():
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip.startswith("192."):
                return ip
    except OSError:
        pass

    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("192.168.1.1", 1))
        ip = probe.getsockname()[0]
        if ip.startswith("192."):
            return ip
    except OSError:
        pass
    finally:
        probe.close()

    return socket.gethostbyname(socket.gethostname())


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
    preferred = int(os.environ.get("PORT", DEFAULT_PORT))
    port = find_free_port(preferred)
    if port != preferred:
        print(f"Port {preferred} is busy, using port {port} instead.")
    server_ip = get_server_ip()
    print(f"Open in browser: http://{server_ip}:{port}")
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
