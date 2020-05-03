import os
from flask import Flask, render_template, request
from sqlalchemy import and_

from models import *


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def main():
    db.create_all()

if __name__=="__main__":
    with app.app_context():
        main()

@app.route("/")
def home():
    return render_template("/Home.html")

@app.route("/Login")
def login():
    return render_template("/Login.html")

@app.route("/Registration")
def registration():
    return render_template("/Registration.html")

@app.route("/confirmation", methods=["POST"])
def regconfirm():
    first_name = request.form.get("FirstName")
    last_name = request.form.get("LastName")
    username = request.form.get("Username")
    existing = Users.query.filter(Users.username == username).all()
    if existing:
        return render_template("/Confirmation.html", Message="Error", confirmationmessage="User already exists")
    password = request.form.get("Password")
    passwordconfirm =request.form.get("Password2")
    if (password != passwordconfirm):
        return render_template("/Confirmation.html", Message="Error", confirmationmessage="Passwords do not match")
    new_user = Users(first_name = first_name, last_name = last_name, username = username, password = password)
    db.session.add(new_user)
    db.session.commit()
    return render_template("/Confirmation.html", Message="Success", confirmationmessage="User Created")

@app.route("/Search", methods=["POST"])
def search():
    username = request.form.get("Username")
    password = request.form.get("Password")
    user = Users.query.filter(and_(Users.username == username, Users.password == password)).all()
    if user:
        return render_template("./Search.html")
    else:
        return render_template("./Confirmation.html", Message="Error", confirmationmessage="Wrong Credentials")

@app.route("/Booktable", methods=["POST"])
def booktable():
    searchmethod = request.form.get("searchmethod")
    searchvalue = request.form.get("search")
    if searchmethod == "ISBN":
        searchtable = Books.query.filter(Books.isbn.like(f"%{searchvalue}%")).all()
    elif searchmethod == "Title":
        searchtable = Books.query.filter(Books.title.like(f"%{searchvalue}%")).all()
    else:
        searchtable = Books.query.filter(Books.author.like(f"%{searchvalue}%")).all()
    if searchtable is None:
        return render_template("./Booktable.html", message = "No such books found")
    else:
        return render_template("./Booktable.html", message = "Please find search results below", books=searchtable)
