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

# Currency formats
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/projects")
def projects():

    if not session.get("user", None):
        return redirect(url_for("login"))

    projects = mongo.db.projects.find()
    user = mongo.db.users.find_one({"user_email": session["user"]})

    return render_template("projects.html", projects=projects, username=user["first_name"])


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
        return redirect(url_for("login"))

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
                    return redirect(url_for("budgets", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect login details")
                return redirect(url_for("login"))
        else:
            flash("Incorrect login details")
            return redirect(url_for("login"))

    return render_template("login.html")
       

@app.route("/logout")
def logout():

    if not session.get("user", None):
        return redirect(url_for("login"))

    # remove user from session cookies
    flash("You have logged out successfully")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/create_project", methods=["GET", "POST"])
def create_project():

    if not session.get("user", None):
        return redirect(url_for("login"))

    if request.method == "POST":

        project_categories = []
       
        for key in request.form.keys():
            if "category" in key:
                name, measure = request.form.getlist(key)
                if not name or not measure:
                    continue
                project_categories.append({"name":name, "measure":measure})

        project = {
            "created_by": session["user"],
            "project_name": request.form.get("project_name"),
            "project_currency": request.form.get("project_currency"),
            "project_start_date": request.form.get("project_start_date"),
            "project_categories": project_categories
        }
        
        mongo.db.projects.insert_one(project)

        flash("Project added successfully!")
        return redirect(url_for("projects"))
    return render_template("create_projects.html")


@app.route("/edit_project/<project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    if not session.get("user", None):
        return redirect(url_for("login"))

    if request.method == "POST":

        project_categories = []
       
        for key in request.form.keys():
            print("KEYS: ", key)            
            if "category" in key:
                print(request.form.getlist(key))
                name, measure = request.form.getlist(key)
                if not name or not measure:
                    continue
                project_categories.append({"name":name, "measure":measure})

        submit = {
            "created_by": session["user"],
            "project_name": request.form.get("project_name"),
            "project_currency": request.form.get("project_currency"),
            "project_start_date": request.form.get("project_start_date"),
            "project_categories": project_categories
    
        }

        mongo.db.projects.update({"_id": ObjectId(project_id)},  submit)
        flash("Project updated successfully!")
        return redirect(url_for("projects"))

    project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    return render_template("edit_project.html", project=project)


@app.route("/delete_project/<project_id>")
def delete_project(project_id):
    if not session.get("user", None):
        return redirect(url_for("login"))

    mongo.db.projects.remove({"_id": ObjectId(project_id)})
    flash("Project deleted successfully!")
    return redirect(url_for("projects"))


@app.route("/budgets")
def budgets():

    if not session.get("user", None):
        return redirect(url_for("login"))

    user = mongo.db.users.find_one({"user_email": session["user"]})

    projects = []

    # Loop over each "project name"
    for project in mongo.db.projects.find({"created_by": session["user"]}):
        data = {
            "_id" : project["_id"],
            "name" : project["project_name"],
            "currency" : project["project_currency"],
            "budgets" : []}
        
        # Loop over each budget that shares "project name"
        for budget_database in mongo.db.budgets.find({"user_email": session["user"], "project_name" : data["name"]}):
            
            budget = {
                "_id": budget_database["_id"],
                "name" : budget_database["budget_name"],
                "categories" : {}
            }

            for i in budget_database["budget_items"]:
                category = i["project_category"].lower()
                if not budget["categories"].get(category, None):
                    budget["categories"][category] = {"items": [i], "total": float(i["amount"])}
                else:
                    
                    budget["categories"][category]["items"].append(i)
                    budget["categories"][category]["total"] += float(i["amount"])
                    
            data["budgets"].append(budget)

        projects.append(data)
    return render_template("budgets.html", projects=projects, user=user)



@app.route("/add_budget/<project_id>", methods=["GET", "POST"])
def add_budget(project_id):
    project = mongo.db.projects.find_one({"_id": ObjectId(project_id), "created_by": session["user"]})
    
    if request.method == "POST":

        budget_items = []
       
        for key in request.form.keys():
            print("KEYS: ", key)            
            if "budget_item" in key:
                print(request.form.getlist(key))
                name, details, amount, category = request.form.getlist(key)
                if not name or not details or not amount or not category:
                    continue
                budget_items.append({"name":name, "details":details, 
                    "amount":amount, "project_category":category })

        submit = {
            "user_email": session["user"],
            "project_name": project["project_name"],
            "budget_name": request.form.get("budget_name"),
            "budget_items": budget_items
    
        }

        mongo.db.budgets.insert_one(submit)
        flash("Budget added successfully!")
        return redirect(url_for("budgets"))

    return render_template("add_budget.html", project=project)


@app.route("/delete_budget/<budget_id>")
def delete_budget(budget_id):
    if not session.get("user", None):
        return redirect(url_for("login"))

    mongo.db.budgets.remove({"_id": ObjectId(budget_id)})
    flash("Budget deleted successfully!")
    return redirect(url_for("budgets"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
