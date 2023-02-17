from flask import Flask, redirect, url_for, render_template, request, session, flash, current_app 
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient


database_login = open("..\\password.txt").read()
app = Flask(__name__, template_folder='templates')
client = MongoClient(database_login)

db = client.flask_db
todos = db.coffee

@app.route("/")
def home():
    data =  todos.find()
    return render_template("home.html", data = data)

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        get_date = str(datetime.utcnow().date())
        get_name = request.form["name"]
        get_mail = request.form["email"]
        todos.insert_one({'name': get_name, 'email': get_mail, 'date':get_date})
        return redirect('/')
    
    else:
        return render_template("form.html")

@app.route("/delete/<page>")
def delete(page):
    todos.delete_one({"_id": ObjectId(page)})
    return redirect('/')


if __name__ == "__main__":
   app.run(debug=True, port=8000)

