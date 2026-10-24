from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

expenses = [
    {"date": "2026-10-20", "category": "Food", "amount": 250},
    {"date": "2026-10-21", "category": "Travel", "amount": 120},
]

@app.route("/")
def home():
    total = sum(e["amount"] for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        expenses.append({"date": date, "category": category, "amount": amount})
        return redirect(url_for("home"))
    return render_template("add.html")