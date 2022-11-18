from flask_app import app
from flask_app.controllers import home_page, login_controller, reviews, book_contact

if __name__ == "__main__":
    app.run(debug=True)
