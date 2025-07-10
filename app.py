from flask import Flask, render_template, request
import time
import logging
import os
import webbrowser
import threading

app = Flask(__name__)
USERNAME = "admin"
PASSWORD = "password123"
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 60

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/attempts.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

attempts = {}
lockout = {}

@app.route("/", methods=["GET", "POST"])
def login():
    ip = request.remote_addr
    now = time.time()
    message = ""
    status = ""

    if ip in lockout and now < lockout[ip]:
        wait = int(lockout[ip] - now)
        status = "locked"
        return render_template("login.html", message=f"⏳ Too many attempts. Try again in {wait}s.", status=status)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            logging.info(f"[{ip}] SUCCESS — Username: {username}")
            attempts[ip] = 0
            status = "success"
            return render_template("login.html", message="✅ Login successful!", status=status)
        else:
            attempts[ip] = attempts.get(ip, 0) + 1
            remaining = MAX_ATTEMPTS - attempts[ip]
            logging.info(f"[{ip}] FAILED — Username: {username}, Password: {password}")
            status = "error"

            if attempts[ip] >= MAX_ATTEMPTS:
                lockout[ip] = now + LOCKOUT_TIME
                status = "locked"
                return render_template("login.html", message="⛔ Account temporarily locked.", status=status)
            else:
                return render_template("login.html", message=f"❌ Invalid credentials. {remaining} attempts left.", status=status)

    return render_template("login.html", message=message, status=status)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
