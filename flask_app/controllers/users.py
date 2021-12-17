from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#localhost:5000 route root
@app.route('/')
def index():

    return render_template("index.html")

# Create Registration - POST request form data and IF INFO VALID redirect to dashboard
@app.route('/register', methods=["POST"])
def create_user():
    # validate information 
    # IF NOT then redirect to '/'
    if not user.User.validate_registration(request.form):
        return redirect('/')

    # IF info valid
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print("PASSWORD IS", pw_hash)

    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    # save user data information
    user_id = user.User.create_user(data)

    # store user id into session
    session['user_id'] = user_id
    return redirect('/dashboard')

# Login route
@app.route('/login', methods = ['POST'])
def login():
    # check if the email provided exists in the database
    user_in_db = user.User.get_by_email(request.form)

    # if no email found
    if not user_in_db:
        flash("Invalid Login Credentials", "login_error")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Login Credentials", "login_error")
        return redirect('/')
    # if login credentials match, set the user_id into session
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

# GET dashboard
@app.route('/dashboard')
def display_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': session['user_id']
    }

    purchases = painting.Painting.get_purchases_by_user(data)
    print("PURCHASES!!!!", purchases)

    return render_template("dashboard.html", user=user.User.get_by_id(data), paintings = painting.Painting.get_all_paintings(), purchases = purchases)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')