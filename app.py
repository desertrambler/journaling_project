from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from flask_cors import CORS

# Setup Flask
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# CORS setup if necessary
CORS(app)

# Initialize Flask-RESTful API
api = Api(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
# Uncomment the next line if running the app for the first time and need to create tables
# db.create_all()

# Resource for Login
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Username and password are required"}, 400

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return {"message": "Login successful"}, 200
        else:
            return {"message": "Invalid username or password"}, 401

# Adding the resource to the API
api.add_resource(LoginResource, '/api/v1/login')

@app.route("/api/v1/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return "Success!"

@app.route("/api/v1/home")
def go_home():
    return render_template("Home.html")

@app.route("/api/v1/sign_up", methods=["POST", "GET"])
def get_sign_up_form():
    if request.method == 'POST':
        username=request.form["signupUsername"],
        password=request.form["signupPassword"],

        if username and password:
            pw_hash = bcrypt.generate_password_hash(password)  # returns bytes
            user = User(username=username, password=pw_hash.decode('utf-8'))  # ✅ decode it
            db.session.add(user)
            db.session.commit()
            return "User created!"
        else:
            return "Missing fields", 422

if __name__ == "__main__":
    app.run(debug=True)