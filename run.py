
import os
import time
from ping3 import ping
from datetime import datetime
from dotenv import load_dotenv
import csv
from db import insert_ping_result, query_history, create_table
from flask import Flask, render_template, request, jsonify
import threading

load_dotenv()
DATABASE = os.environ.get("DATABASE_URL", "data/database.sqlite3")
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", 60))

create_table(DATABASE)

app = Flask(__name__, template_folder=".")

def ping_ip(ip: str, timeout:float=2) -> float | None:
    result = ping(ip, timeout=timeout, unit='ms')
    print(result)
    return result if isinstance(result, (int, float)) else None

def get_ip_list_full():
    csv_path = os.path.join(os.path.dirname(__file__), 'data/server.csv')
    ip_list = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip = row.get('ip')
                name = row.get('name')
                if ip:
                    ip_list.append({"ip": ip, "name": name})
    return ip_list

def monitor():
    while True:
        ip_list = get_ip_list_full()
        # 统一用 UTC 时间
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        for item in ip_list:
            ip = item["ip"]
            latency = ping_ip(ip)
            insert_ping_result(DATABASE, ip, latency, timestamp)
        time.sleep(PING_INTERVAL)

@app.route("/")
def index():
    return render_template("template.html")
@app.route("/api/ips")
def api_ips():
    return jsonify(get_ip_list_full())

@app.route("/history")
def history():
    ips = request.args.get("ips")
    period = request.args.get("period", "day")
    if ips:
        ip_list = ips.split(",")
        result = query_history(DATABASE, ip_list, period)
        return jsonify(result)
    else:
        ip = request.args.get("ip")
        data = query_history(DATABASE, [ip], period)
        return jsonify(data)

def start_monitor():
    t = threading.Thread(target=monitor, daemon=True)
    t.start()

if __name__ == "__main__":
    start_monitor()
    app.run(host="0.0.0.0", port=5000,debug=True if os.getenv("FLASK_ENV") == "development" else False)
