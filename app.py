from flask import Flask, redirect, url_for, render_template, request, session, flash, current_app 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite3"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    def __init__(self, username, email):
        self.username = username
        self.email = email
    

@app.route("/")
def home():
    data = User.query.order_by(desc(User.date))
    for i in data:
        print(i.date.date())
    return render_template("home.html", data = data)

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        get_name = request.form["name"]
        get_mail = request.form["email"]
        new_data = User(username=get_name, email = get_mail)

        try:
            db.session.add(new_data)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("form.html")


if __name__ == "__main__":
   with app.app_context():
        db.create_all()
   app.run(debug=True, port=8000)

