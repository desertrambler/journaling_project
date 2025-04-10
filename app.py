from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import g
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

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

@app.route("/", methods=["GET"])
def login_user():
    return render_template("Login.html")

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return "Success!"

@app.route("/users/read", methods=["GET"])
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    for user in users:
        print(user.id, user.username, user.password)
    return "hello"

@app.route("/home")
def home():
    return render_template("Home.html")

@app.route("/sign_up/", methods=["POST", "GET"])
def get_sign_up_form():
        if request.method == "POST":
            sign_up_form = '''
                  <div id="signupContainer" class="max-w-sm w-full bg-red-900 p-6 rounded-lg shadow-lg">
                    <h2 class="text-3xl font-extrabold text-center mb-6">Login</h2>
                    <form x-target="signupContainer" method="get" action="/sign_up/">
                    <!-- Username -->
                    <div class="mb-4">
                        <label for="username" class="block text-lg font-medium text-white mb-2">Username</label>
                        <input type="text" id="username" name="username" class="w-full p-3 border border-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500" required>
                    </div>
            
                    <!-- Password -->
                    <div class="mb-6">
                        <label for="password" class="block text-lg font-medium text-white mb-2">Password</label>
                        <input type="password" id="password" name="password" class="w-full p-3 border border-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500" required>
                    </div>
            
                    <!-- Submit Button -->
                    <div class="flex justify-center">
                        <button type="submit" class="w-full py-3 bg-red-700 text-white font-bold rounded-md hover:bg-red-600 transition-colors duration-300">
                        Log In
                        </button>
                    </div>
                    </form>
            
                    <!-- Forgot Password Link -->
                    <div class="mt-4 text-center">
                    <a href="#" class="text-sm text-white hover:text-gray-400">Forgot password?</a>
                    </div>
                </div>
            '''
            return sign_up_form
        else:
            user = User(
                username=request.form["username"],
                password=request.form["password"],
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('/'))



if __name__ == "__main__":
    app.run(debug=True)