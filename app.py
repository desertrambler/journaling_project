from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use a relative path for SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable the modification tracking feature to save resources

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define a model for your database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("hello")
    else:
        return render_template("Login.html")

@app.route("/home")
def home():
    return render_template("Home.html")


if __name__ == "__main__":
    app.run(debug=True)