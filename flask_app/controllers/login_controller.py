from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/registration', methods=['POST'])
def registration():
    print('hello')
    if not User.validate_registration(request.form): #returns boolean (true or false) so here it says if survey is not valid then return it to the index.
        return redirect('/login_page')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["login_email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/login_page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'login')
        return redirect('/login_page')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/")



@app.route('/logout')
def logout():
    session.clear()
    session['authorize'] = False
    return redirect('/')