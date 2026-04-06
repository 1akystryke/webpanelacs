from flask import Flask, jsonify, request,send_file

import os
import threading
import time

app = Flask(__name__)

def _get_env():
    return {
        "server_path": os.getenv("SERVER_PATH", ""),
        "port": int(os.getenv("PORT", "5000")),
    }

# ----------------------
# Mock server state
# ----------------------
server_state = {
    "status": "OFFLINE",
    "uptime": 0,
    "players": 0,
    "maxPlayers": 16,
    "track": "monza",
    "sessionType": "RACE"
}

session_state = {
    "track": "monza",
    "layout": "gp",
    "cars": ["ks_ferrari_488_gt3"],
    "slots": 16,
    "sessionType": "RACE",
    "weather": {
        "ambientTemp": 26,
        "roadTemp": 32
    }
}

cars_list = [
    {"id": "ks_ferrari_488_gt3", "name": "Ferrari 488 GT3"},
    {"id": "ks_bmw_m4_gt3", "name": "BMW M4 GT3"},
    {"id": "chetyrka", "name": "лада ебать четырнадцать"}
]

tracks_list = [
    {"id": "monza", "layouts": ["gp", "junior"]},
    {"id": "spa", "layouts": ["default"]}
]

logs = []

# ----------------------
# Background uptime
# ----------------------
def uptime_worker():
    while True:
        if server_state["status"] == "ONLINE":
            server_state["uptime"] += 1
        time.sleep(1)

threading.Thread(target=uptime_worker, daemon=True).start()

# ----------------------
# Server endpoints
# ----------------------
@app.route("/api/server/status")
def get_status():
    return jsonify(server_state)

@app.route("/api/server/start", methods=["POST"])
def start_server():
    server_state["status"] = "ONLINE"
    logs.append("Server started")
    return jsonify({"success": True})

@app.route("/api/server/stop", methods=["POST"])
def stop_server():
    server_state["status"] = "OFFLINE"
    server_state["uptime"] = 0
    logs.append("Server stopped")
    return jsonify({"success": True})

# ----------------------
# Session endpoints
# ----------------------
@app.route("/api/session")
def get_session():
    return jsonify(session_state)

@app.route("/api/session", methods=["PUT"])
def update_session():
    data = request.json
    session_state.update(data)
    logs.append("Session updated")
    return jsonify({"success": True})

# ----------------------
# Cars & Tracks
# ----------------------
@app.route("/api/cars")
def get_cars():
    return jsonify(cars_list)

@app.route("/api/tracks")
def get_tracks():
    return jsonify(tracks_list)

# ----------------------
# Players (mock)
# ----------------------
@app.route("/api/players")
def get_players():
    return jsonify([
        {
            "name": "Player1",
            "car": "ks_ferrari_488_gt3",
            "lapTime": 123.45,
            "ping": 42
        }
    ])

# ----------------------
# Logs
# ----------------------
@app.route("/api/logs")
def get_logs():
    limit = int(request.args.get("limit", 100))
    return jsonify(logs[-limit:])

# ----------------------
# WEB APP
# ----------------------
@app.route("/")
def index():
    return send_file("vue/index.html")


# ----------------------
# Run
# ----------------------
if __name__ == "__main__":
    env = _get_env()
    app.run(host="0.0.0.0")