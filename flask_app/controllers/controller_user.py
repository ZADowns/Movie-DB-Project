from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_movie import Movie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/register/user', methods=['POST'])
def new_User():
    if not User.validate_user(request.form):
        return redirect('/')
    
    
    if User.check_email(request.form) == True:
        flash("User already exists!", 'reg')
        return redirect('/')
    #validate other parts of the form
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if session.get('user_id') != None:
        data = {
            "id" : session['user_id']
        }
        return render_template("dashboard.html", user=User.get_one(data), movies = Movie.get_all_movies())
    else:
        return render_template("dashboard.html", movies = Movie.get_all_movies())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/loginpage")
def loginpage():
    return render_template("index.html")