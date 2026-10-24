from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key(forthedevs)'

def get_db():
    connection = sqlite3.connect('expenses.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def home():
    db = get_db()
    expenses = db.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    db.close()
    total = sum(e["amount"] for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        db = get_db()
        db.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
        db.commit()
        db.close()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            error = "Username and password are required."
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password, method="pbkdf2:sha256")),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = "That username is already taken."
            finally:
                db.close()

            if error is None:
                return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Wrong username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))