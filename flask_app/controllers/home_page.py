from flask_app import app
from flask import render_template, request, redirect,session
from flask_app.models.user import User


@app.route('/')
def index():
    if not session.get('user_id'):
        return render_template('index.html', user = None)
    data = {
        'id': session['user_id']
    }
    session['authorized'] = True
    
    user = User.get_by_id(data)
    return render_template('index.html', user = user)


@app.route('/about')
def about():
    if not session.get('user_id'):
        return render_template('about.html', user = None)
    data = {
        'id': session['user_id']
    }
    session['authorized'] = True
    
    user = User.get_by_id(data)
    return render_template('about.html', user = user)

