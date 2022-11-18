from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r"^(?=.*?[A-Z])(?=.*?[0-9]).{8,}$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('car_wash_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, first_name, last_name, email, password, created_at, updated_at) VALUES ( %(username)s, %(first_name)s ,  %(last_name)s ,  %(email)s,  %(password)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        result =  connectToMySQL('car_wash_schema').query_db( query, data )
        return result

    @staticmethod
    def validate_registration(user):
        print('no working')
        is_valid = True #we assume that survey is valid
        query = "SELECT email FROM users WHERE email = %(email)s;"
        results = connectToMySQL('car_wash_schema').query_db(query, user)
        # test whether a field matches the pattern
        if len(results) >= 1:
            flash("Email Already Taken", 'register')
            is_valid= False
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid password!", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Password doesn't match!" , 'register')
            is_valid = False
        return is_valid

#------------------------
#methods to log in the user
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("car_wash_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("car_wash_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])