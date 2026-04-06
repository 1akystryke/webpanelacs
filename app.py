from flask import Flask, jsonify
import os

app = Flask(__name__)


def _get_env():
    return {
        "server_path": os.getenv("SERVER_PATH", ""),
        "port": int(os.getenv("PORT", "5000")),
    }


@app.get("/")
def index():
    env = _get_env()
    return jsonify(
        status="ok",
        server_path=env["server_path"],
        message="AC server controller is running",
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    env = _get_env()
    app.run(host="0.0.0.0")
