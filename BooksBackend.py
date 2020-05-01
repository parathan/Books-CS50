from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def start():
    return render_template("Home.html")

@app.route("/Login")
def login():
    return render_template("Login.html")

@app.route("/Registration")
def registration():
    return render_template("Registration.html")
