from flask.templating import render_template
from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, paintings
from flask import flash
import re 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    db_name = 'paintings'

    # constructor
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #instance method
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # class methods
    # CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # READ
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        print("GET BY EMAIL", result)

        # if no email is found
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        print("RESULT IS", result)

        # if no id found
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # validate registration data
    @staticmethod
    def validate_registration(user):
        is_valid = True

        # run a query to get all emails in database
        query = "SELECT * FROM users WHERE email = %(email)s;"    
        results = connectToMySQL(User.db_name).query_db(query, user)
        # email validations
        if len(results) >= 1:
            flash("Email already taken.", "reg_error")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Please enter valid email address", "reg_error")
            is_valid = False

        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "reg_error")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "reg_error")
            is_valid = False

        # checking if passwords match    
        if user['password'] != user['password_confirm']:
            is_valid = False
            flash("Passwords do not match", "reg_error")
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "reg_error")
            is_valid = False
        # check to see if there is at least one letter and one number
        elif bool(re.match('^.*(?=.*\d)(?=.*[a-zA-Z]).*$', (user['password']))) == False:
            is_valid = False
            flash("Password must include one letter and one number")
        
        return is_valid

    
    # validate login data
    @staticmethod
    def validate_login(user):
        is_valid = True

        # run a query to get all emails in database
        query = "SELECT * FROM users WHERE email = %(email)s"    
        results = connectToMySQL(User.db_name).query_db(query, user)

        if len(results) < 1: # no users are found
            is_valid = False
            flash("Invalid login credentials.", "login_error")
    

        return is_valid
