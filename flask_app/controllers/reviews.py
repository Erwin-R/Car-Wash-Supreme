from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.review import Review


@app.route('/reviews')
def reviews():
    reviews = Review.get_all()
    if not session.get('user_id'):
        return render_template('reviews.html', user = None, reviews = reviews)
    data = {
        'id': session['user_id']
    }
    session['authorized'] = True
    user = User.get_by_id(data)
    return render_template('reviews.html', user = user, reviews = reviews)


@app.route('/new_review')
def new_review():
    if not session.get('user_id'):
        return render_template('new_review.html', user = None)
    data = {
        'id' : session['user_id']
    }
    logged_in_user = User.get_by_id(data)
    return render_template('new_review.html', user = logged_in_user)
    

@app.route('/create_review', methods=['POST'])
def create_review():
    if not Review.validate_review(request.form):
        print('helo')
        return redirect('/new_review')
    
    data ={
        **request.form,
        'user_id': session['user_id']
    }

    Review.create(data)

    return redirect('/reviews')


@app.route('/edit_review/<int:review_id>')
def edit(review_id):
    data = {
        "id": review_id
    }

    review = Review.get_by_id(data)
    user = User.get_by_id({"id" : session['user_id']})
    return render_template("edit_review.html", review = review, user = user)


@app.route('/update_review/<int:review_id>', methods=['POST'])
def update(review_id):
    if not Review.validate_review(request.form):
        return redirect(f'/edit_review/{review_id}')
    
    data = {
        **request.form,
        'id' : review_id
    }
    Review.update(data)
    return redirect('/reviews')


@app.route('/delete_review/<int:review_id>')
def delete(review_id):
    data = {
        'id' : review_id
    }
    Review.delete(data)
    return redirect('/reviews')