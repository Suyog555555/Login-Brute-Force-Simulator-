from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"
MAX_ATTEMPTS = 3
attempts = 0
is_locked = False

@app.route("/", methods=["GET", "POST"])
def login():
    global attempts, is_locked

    message = ""

    if is_locked:
        message = "🔒 Account is locked due to too many failed attempts."
        return render_template("login.html", message=message)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            message = "✅ Login successful! Welcome!"
            attempts = 0  # Reset after success
        else:
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            if remaining <= 0:
                is_locked = True
                message = "🔒 Account locked after 3 failed attempts."
            else:
                message = f"❌ Invalid credentials. {remaining} attempts left."

    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
