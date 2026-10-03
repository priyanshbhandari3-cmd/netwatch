from flask import Flask, request, render_template
import socket, time, requests
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
history = []

def clean(host):
    host = host.strip()
    if "://" in host:
        host = urlparse(host).netloc
    return host.split("/")[0]

def port_open(host, port):
    try:
        socket.create_connection((host, port), timeout=3).close()
        return True
    except Exception:
        return False

def check(host):
    res = {"host": host, "ip": None, "status": "DOWN", "code": "-",
           "ms": None, "p80": False, "p443": False, "tip": "",
           "time": datetime.now().strftime("%d %b %Y, %H:%M:%S")}
    try:
        res["ip"] = socket.gethostbyname(host)
    except Exception:
        res["tip"] = "DNS resolution failed: domain name is wrong or DNS is not responding."
        return res
    res["p80"] = port_open(host, 80)
    res["p443"] = port_open(host, 443)
    for scheme in ("https://", "http://"):
        try:
            t = time.time()
            r = requests.get(scheme + host, timeout=5)
            res["ms"] = round((time.time() - t) * 1000)
            res["code"] = r.status_code
            res["status"] = "UP"
            break
        except Exception:
            continue
    if res["status"] == "UP":
        res["tip"] = ("Website is reachable and working normally."
                      if res["ms"] < 1000 else
                      "High latency: possible congestion or a slow server.")
    elif not res["p80"] and not res["p443"]:
        res["tip"] = "Ports 80 and 443 are closed: web service is stopped or a firewall is blocking it."
    else:
        res["tip"] = "Port is open but the HTTP request failed: web application may be misconfigured."
    return res

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        host = clean(request.form.get("host", ""))
        if host:
            result = check(host)
            history.insert(0, result)
            del history[10:]
    return render_template("index.html", r=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)