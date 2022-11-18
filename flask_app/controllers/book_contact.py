from flask_app import app
from flask_mail import Message, Mail
from flask import render_template, request, redirect,session
from flask_app.models.user import User

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rerwin684@gmail.com'
app.config['MAIL_PASSWORD'] = 'tzlgvjbqorbmbvmu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/book", methods=['POST'])
def book():
    msg = Message(
                'Appointment Confirmed',
                sender ='rerwin684@gmail.com',
                recipients = ['rerwin684@gmail.com']
        )
    msg.body = f"Appointment booked for {request.form['service-date']} for a {request.form['car_type']} and will be returned by {request.form['return-date']}."
    # msg.body = "testing email"
    mail.send(msg)
    return redirect('/')

@app.route('/contact')
def contact():
    if not session.get('user_id'):
        return render_template('contact.html', user = None)
    data = {
        'id': session['user_id']
    }
    session['authorized'] = True
    
    user = User.get_by_id(data)
    return render_template('contact.html', user = user)

@app.route("/contact_post", methods=['POST'])
def contact_post():
    msg = Message(
                'Customer Inquiry',
                sender ='rerwin684@gmail.com',
                recipients = ['rerwin684@gmail.com']
        )
    msg.body = f"{request.form['first_name']} {request.form['last_name']} preferred contact method is {request.form['contact']}.You can email them at {request.form['email']} or call them at {request.form['phone-num']}. These are their comments: {request.form['comments']}"
    # msg.body = "testing email"
    mail.send(msg)
    return redirect('/contact')