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
        data = request.get_json()  # Get the JSON data from the request body
        
        # Extract username and password
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        # Query the user by username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Login successful"}), 200
        else:
            print("help!")
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
        if request.method == "GET":
            sign_up_form = '''
                  <div id="signupContainer" class="max-w-sm w-full bg-red-900 p-6 rounded-lg shadow-lg">
                    <h2 class="text-3xl font-extrabold text-center mb-6">Login</h2>
                    <form 
                        method="post" 
                        action="/sign_up"
                        x-data="{ signupPassword: '', signUpconfirmation: '', matches: true }"
                        @submit="if (!matches) { $event.preventDefault(); alert('Passwords do not match!') }"                        
                        x-init="$watch('signUpconfirmation', () => matches = signupPassword === signUpconfirmation)"
                        >
                    <!-- Username -->
                    <div class="mb-4">
                        <label for="signupUsername" class="block text-lg font-medium text-white mb-2">Username</label>
                        <input type="text" id="signupUsername" name="signupUsername" class="w-full p-3 border border-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500" required>
                    </div>
            
                    <!-- Password -->
                    <div class="mb-6">
                        <label for="password" class="block text-lg font-medium text-white mb-2">Password</label>
                        <input type="password" x-model="signupPassword" id="signupPassword" name="signupPassword" class="w-full p-3 border border-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500" minLength="8" required>
                    </div>

                    <div class="mb-6">
                        <label for="confimation" class="block text-lg font-medium text-white mb-2">Confirm Password</label>
                        <input type="password" x-model="signUpconfirmation" id="signUpconfirmation" name="signUpconfirmation" class="w-full p-3 border border-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500" required>
                    </div>
            
                    <!-- Submit Button -->
                    <div class="flex justify-center">
                        <button 
                            :disabled="!matches"
                            x-on:click="document.getElementById('signupUsername').required = false;document.getElementById('signupPassword').required = false;window.location.reload()" 
                            class="w-full py-3 bg-red-700 text-white font-bold rounded-md hover:bg-red-600 transition-colors duration-300">
                        Return to Log In
                        </button>
                    </div>

                    <!-- Submit Button -->
                    <div class="flex justify-center mt-5">
                        <button type="submit" class="w-full py-3 bg-red-700 text-white font-bold rounded-md hover:bg-red-600 transition-colors duration-300">
                        Sign Up
                        </button>
                    </div>
                    </form>
                </div>
            '''
            return sign_up_form
        else:
            user = User(
                username=request.form["signupUsername"],
                password=request.form["signupPassword"],
            )
            if user.username and user.password:
                pw_hash = bcrypt.generate_password_hash(user.password, 12)
                user.password = str(pw_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login_user'))
            else:
                return 422


if __name__ == "__main__":
    app.run(debug=True)