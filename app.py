from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
        db.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",(date, category, amount))
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