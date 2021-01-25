import os
from flask import (Flask, flash, render_template, 
                    redirect, request, session, 
                    url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
@app.route("/projects")
def projects():
    projects = mongo.db.projects.find()
    return render_template("projects.html", projects=projects)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if email address already exists
        existing_email = mongo.db.users.find_one(
            {"user_email": request.form.get("email").lower()})
        
        if existing_email:
            flash("That email address is already registered, please try again")
            return redirect(url_for("register"))
        
        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "user_email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put new user email address into session cookie
        session["user"] = request.form.get("email").lower()
        flash("You have registered successfully!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if email address already exists
        existing_email = mongo.db.users.find_one(
            {"user_email": request.form.get("email").lower()})

        if existing_email:
            # check to see if password entered by user matches hashed password in db
            if check_password_hash(
                existing_email["password"], request.form.get("password")):
                    session["user"] = request.form.get("email").lower()
                    flash("Welcome, {}!".format(
                        existing_email["first_name"].capitalize()))
                    return redirect(url_for("dashboard", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect login details")
                return redirect(url_for("login"))
        else:
            flash("Incorrect login details")
            return redirect(url_for("login"))

    return render_template("login.html")
       

@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    username = mongo.db.users.find_one({"user_email": session["user"]})["first_name"]
    return render_template("dashboard.html", username=username)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
