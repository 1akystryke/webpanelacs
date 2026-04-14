from flask import Flask, jsonify, request, send_file, session, redirect, url_for, render_template

import os
import secrets
from core.core import Core
import time
import requests
import zipfile
from werkzeug.utils import secure_filename
import shutil



# PATH = os.getenv("SERVER_PATH", "")
PATH = "/ac_server"

app = Flask(__name__, template_folder="vue")
server_controller = Core(server_path=PATH)

app.secret_key = os.getenv("SESSION_SECRET", "dev-insecure-secret")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"

UPLOAD_FOLDER = "uploads"
EXTRACT_FOLDER = "mods"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

def _get_env():
    return {
        "server_path": os.getenv("SERVER_PATH", ""),
        "port": int(os.getenv("PORT", "5000"))
    }

def _get_auth_env():
    return {
        "username": os.getenv("AUTH_USER", ""),
        "password": os.getenv("AUTH_PASS", ""),
    }

login_attempts = {}
LOGIN_WINDOW_SECONDS = 300
LOGIN_MAX_FAILS = 5
LOGIN_BLOCK_SECONDS = 300

def _get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"

def _login_is_blocked(ip):
    record = login_attempts.get(ip)
    if not record:
        return False
    return record.get("blocked_until", 0) > time.time()

def _record_login_failure(ip):
    now = time.time()
    record = login_attempts.setdefault(ip, {"fails": [], "blocked_until": 0})
    record["fails"] = [t for t in record["fails"] if now - t < LOGIN_WINDOW_SECONDS]
    record["fails"].append(now)
    if len(record["fails"]) >= LOGIN_MAX_FAILS:
        record["blocked_until"] = now + LOGIN_BLOCK_SECONDS

def _clear_login_failures(ip):
    if ip in login_attempts:
        login_attempts.pop(ip, None)

def _ensure_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token

def _validate_csrf(token):
    return token and session.get("csrf_token") == token

def _is_logged_in():
    return session.get("auth") is True

def safe_extract(zip_ref, path):
    for member in zip_ref.namelist():
        member_path = os.path.join(path, member)

        if not os.path.realpath(member_path).startswith(os.path.realpath(path)):
            raise Exception("Попытка path traversal!")

    zip_ref.extractall(path)

def validate_mod_structure(path):
    content_path = os.path.join(path, "content")

    if not os.path.isdir(content_path):
        return False

    cars_path = os.path.join(content_path, "cars")
    tracks_path = os.path.join(content_path, "tracks")

    # хотя бы что-то должно быть
    if not (os.path.isdir(cars_path) or os.path.isdir(tracks_path)):
        return False

    return True

def if_mod_is_car(path):
    for a in os.listdir(path):
        data_acd_path = path+f"/{a}/data.acd"
        #print(data_acd_path)
        break

    
    if not os.path.exists(data_acd_path):
        return False, path+f"/{a}"
    return True, path+f"/{a}"

def move_mod_as_car(mod_path,server_path):
    target_path = server_path+"/content/cars"
    shutil.move(mod_path,target_path)

def move_mod_as_track(mod_path,server_path):
    target_path = server_path+"/content/tracks"
    shutil.move(mod_path,target_path)
    

@app.before_request
def require_login():
    if request.path.startswith("/api/") or request.path == "/":
        if not _is_logged_in():
            if request.path.startswith("/api/"):
                return jsonify({"error": "unauthorized"}), 401
            return redirect(url_for("login", next=request.path))
    if request.path == "/login" and _is_logged_in():
        return redirect("/")
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if request.path.startswith("/api/") or request.path in {"/logout", "/login"}:
            token = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
            if not _validate_csrf(token):
                if request.path.startswith("/api/"):
                    return jsonify({"error": "csrf"}), 400
                return redirect(url_for("login", error="3"))


logs = []


# ----------------------
# Server endpoints
# ----------------------

@app.route("/api/server/start", methods=["POST"])
def start_server():
    res,err = server_controller.supervisor_start()
    if res!="acserver: started":
        return jsonify({"success": False,"error":err})
    return jsonify({"success": True})

@app.route("/api/server/stop", methods=["POST"])
def stop_server():
    res,err = server_controller.supervisor_stop()
    if res!="acserver: stopped":
        return jsonify({"success": False,"error":err})
    return jsonify({"success": True})

# ----------------------
# Session endpoints
# ----------------------
@app.route("/api/session")
def get_session():
    session_state = server_controller.get_session_state()
    return jsonify(session_state)

@app.route("/api/session", methods=["PUT"])
def update_session():
    data = request.json

    server_controller.set_car_list(data["cars"])
    server_controller.apply_session(data)
    res,err = server_controller.supervisor_restart()
    if res!="acserver: stopped\nacserver: started" and res!="acserver: ERROR (not running)\nacserver: started":
        return jsonify({"success": False,"error":err})
    # if res!="acserver: stopped":
    #     
    return jsonify({"success": True})

# ----------------------
# Cars & Tracks
# ----------------------
@app.route("/api/cars")
def get_cars():
    cars_list = server_controller.list_cars()
    return jsonify(cars_list)

@app.route("/api/tracks")
def get_tracks():
    tracks_list = server_controller.list_tracks()
    return jsonify(tracks_list)

@app.route("/api/weather")
def get_weather():
    weather = server_controller.list_weathers()
    return jsonify(weather)


# -----------------------------
# MOD UPLOAD
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_mod():
    if "mod" not in request.files:
        return jsonify({"error": "Нет файла"}), 400

    file = request.files["mod"]

    if file.filename == "":
        return jsonify({"error": "Пустое имя файла"}), 400

    filename = secure_filename(file.filename)
    zip_path = os.path.join(UPLOAD_FOLDER, filename)

    # сохраняем ZIP
    file.save(zip_path)

    # папка для распаковки
    extract_path = os.path.join(EXTRACT_FOLDER, filename.replace(".zip", ""))
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            safe_extract(zip_ref, extract_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # валидация структуры
    is_car,cont_path = if_mod_is_car(extract_path)
    
    if is_car:
        move_mod_as_car(cont_path,PATH)
    else:
        move_mod_as_track(cont_path,PATH)


    return jsonify({"status": "ok"})



# ---------------------
# INFO
# ---------------------

@app.route("/api/info")
def get_info():
    url = "http://localhost:8081/INFO"

    payload = {}
    headers = {
      'Content-Type': 'application/json'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        json_clone = response.json()
        json_clone["status"]="online"
        return json_clone,200
    except:
        return {"status":"offline"},200

@app.route("/api/entry")
def get_entry():


    url = "http://localhost:8081/ENTRY"

    payload = {}
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    html = response.text
    with open("vue/framecss.html") as f:
        css = f.read()
    index = html.find("<head>")
    html = html[:index+6]+css+html[index+6:]
    return html,200

# ----------------------
# Logs
# ----------------------


@app.route("/api/logs")
def get_logs():
    limit = int(request.args.get("limit", 100))
    logs = server_controller.get_ac_server_logs()
    return jsonify({"logs":logs[-limit:]})

@app.route("/api/csrf")
def get_csrf():
    return jsonify({"token": _ensure_csrf_token()})

# ----------------------
# WEB APP
# ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        csrf_token = _ensure_csrf_token()
        return render_template("login.html", csrf_token=csrf_token)
    ip = _get_client_ip()
    if _login_is_blocked(ip):
        return redirect(url_for("login", error="2"))
    auth_env = _get_auth_env()
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == auth_env["username"] and password == auth_env["password"] and username:
        session["auth"] = True
        _clear_login_failures(ip)
        next_url = request.form.get("next") or request.args.get("next") or "/"
        return redirect(next_url)
    _record_login_failure(ip)
    return redirect(url_for("login", error="1"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    return send_file("vue/index.html")


# ----------------------
# Run
# ----------------------
if __name__ == "__main__":
    env = _get_env()
    app.run(host="0.0.0.0")

