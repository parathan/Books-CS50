import os
from flask import Flask, render_template, request
from sqlalchemy import and_

from models import *


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://llsimqlrbzioru:cb67ae337584aa335aa569e499e5bcfaf76517d7f744a02f363a553ff8e90a52@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d2jj16lvup4u56"
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
        return render_template("./Search.html", username=username)
    else:
        return render_template("./Confirmation.html", Message="Error", confirmationmessage="Wrong Credentials")

@app.route("/Booktable/<username>", methods=["POST"])
def booktable(username):
    searchmethod = request.form.get("searchmethod")
    searchvalue = request.form.get("search")
    if searchmethod == "ISBN":
        searchtable = Books.query.filter(Books.isbn.like(f"%{searchvalue}%")).all()
    elif searchmethod == "Title":
        searchtable = Books.query.filter(Books.title.like(f"%{searchvalue}%")).all()
    else:
        searchtable = Books.query.filter(Books.author.like(f"%{searchvalue}%")).all()
    if searchtable is None:
        return render_template("./Booktable.html", message = "No such books found", username=username)
    else:
        return render_template("./Booktable.html", message = "Please find search results below", books=searchtable, username=username)

@app.route("/book/<username>/<int:book_id>")
def book(book_id, username):
    book = Books.query.get(book_id)
    reviews = Reviews.query.filter(Reviews.title==book.title).all()
    return render_template("./Book.html", book=book, username=username, reviews=reviews)

@app.route("/Searchagain/<username>/<bookname>", methods=["POST"])
def review(bookname, username):
    rawrating = request.form.get("rating")
    rating = int(rawrating)
    review = request.form.get("review")
    new_review = Reviews(username=username, title=bookname, rating=rating, review=review)
    db.session.add(new_review)
    db.session.commit()
    return render_template("./Search.html", username=username)
