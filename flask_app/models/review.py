from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import flask_app.models.user as user_model


class Review:
    def __init__( self , data ):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.date = data['date']
        self.satisfaction = data['satisfaction']
        self.recommend = data['recommend']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews JOIN users ON users.id = reviews.user_id;"
        results = connectToMySQL('car_wash_schema').query_db(query)
        reviews = []
        for result in results:
            review = cls(result)
            user_data = {
                **result,
                "id" : result['users.id'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at'],
            }
            user = user_model.User(user_data)
            review.user = user
            reviews.append(review)
        return reviews

    @classmethod
    def create(cls, data):
        query = "INSERT INTO reviews (customer_name, date, satisfaction, recommend, comments, created_at, user_id)" 
        query += "VALUES ( %(customer_name)s ,  %(date)s ,  %(satisfaction)s,  %(recommend)s, %(comments)s, NOW(), %(user_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        result =  connectToMySQL('car_wash_schema').query_db( query, data )
        return result

    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['customer_name']) < 3:
            flash("Name must be at least 3 characters.", 'create')
            is_valid = False
        if review['date'] == "":
            flash("Please pick a date.", 'create')
            is_valid = False
        if len(review['satisfaction']) < 1:
            flash("Must choose an option.", 'create')
            is_valid = False
        if len(review['recommend']) < 1:
            flash("Must choose an option.", 'create')
            is_valid = False
        if len(review['comments']) < 10:
            flash("Comments must be at least 10 characters.", 'create')
            is_valid = False
        return is_valid


    @classmethod    
    def get_by_id(cls,data):
        query = "SELECT * FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.id = %(id)s;"
        result = connectToMySQL("car_wash_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        row = result[0]
        review = cls(result[0])
        user_data = {
            **row,
            "id" : row['users.id'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at']
        }
        user= user_model.User(user_data)
        review.user = user
        return review

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET customer_name = %(customer_name)s, date = %(date)s , satisfaction = %(satisfaction)s, recommend = %(recommend)s, comments = %(comments)s, updated_at = NOW() WHERE id = %(id)s;" #the id is coming from the hidden input
        return connectToMySQL('car_wash_schema').query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL('car_wash_schema').query_db(query, data)