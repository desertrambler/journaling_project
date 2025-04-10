from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import g
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_bcrypt import Bcrypt
from flask_cors import CORS

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

bcrypt = Bcrypt(app)

"""
READ THIS:
- flask db migrate -m "Added user table"
- flask db upgrade
- (if you mess up) flask db downgrade
"""

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=False)

# with app.app_context():
   #  db.create_all()

@app.route("/api/v1/login", methods=["POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()

        for user in users:
            if user.username == username:
                p_to_decrypt = user.password
                if bcrypt.check_password_hash(p_to_decrypt, user.password):
                    return 200
                else:
                    return 401

@app.route("api/v1/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return "Success!"

@app.route("api/v1/users/read", methods=["GET"])
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    for user in users:
        print(user.id, user.username, user.password)
    return "hello"

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
                pw_hash = bcrypt.generate_password_hash(user.password)
                user.password = str(pw_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login_user'))
            else:
                return 422


if __name__ == "__main__":
    app.run(debug=True)