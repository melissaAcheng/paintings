from flask.templating import render_template
from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, paintings
from flask_app.models import user
from flask import flash

class Painting:

    db_name = 'paintings'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.artist = None
        self.buyer = None

    # class methods
    # create new painting
    @classmethod
    def create_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, quantity, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s);"

        return connectToMySQL(cls.db_name).query_db(query, data)



    # read - get all paintings
    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings JOIN users as artists on artists.id = user_id;"
        results = connectToMySQL(cls.db_name).query_db(query) # returns list of dict

        print("ALL PAINTINGS===", results)
        all_paintings = [] # create a list to append paintings in
        # GOAL is to create of list of objects

        for row in results:
            this_painting = cls(row)
            

            user_info = {
                'id': row['artists.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['artists.created_at'],
                'updated_at': row['artists.updated_at'],
            }

            #instantiate user_info
            this_user = user.User(user_info)
            this_painting.artist = this_user

            # append to all_paintings list
            all_paintings.append(this_painting)



        return all_paintings


    # read - get one painting by id
    @classmethod
    def get_one_painting(cls, data):
        query = "SELECT * FROM paintings JOIN users as artists on artists.id = user_id WHERE paintings.id = %(id)s"

        results = connectToMySQL(cls.db_name).query_db(query, data)
        print("GET ONE====", results)

        this_painting = cls(results[0])
        this_painting.artist = user.User.get_by_id({'id': results[0]['user_id']})

        return this_painting

    # get all painting purchases by session user
    @classmethod
    def get_purchases_by_user(cls, data):
        query = "SELECT * FROM purchases JOIN paintings ON painting_id = paintings.id JOIN users as buyers ON purchases.user_id = buyers.id JOIN users as artists ON paintings.user_id = artists.id WHERE buyers.id = %(id)s;"

        results = connectToMySQL(cls.db_name).query_db(query, data)
        print("WHICH PAINTINGS???", results)
        # print("RESULTS", results)

        all_purchases = []

        if len(results) < 1:
            return results
        else:
            for row in results:
                this_painting = cls(row)
                print ("????==============", row)
                # print("LENGTH RESULTS===", len(results))

                this_painting.painting_id = row['painting_id']
                
                buyer_info = {
                    'id': row['buyers.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['buyers.created_at'],
                    'updated_at': row['buyers.updated_at'],
                }

                this_buyer = user.User(buyer_info)
                this_painting.buyer = this_buyer
                
                artist_info = {
                    'id': row['artists.id'],
                    'first_name': row['artists.first_name'],
                    'last_name': row['artists.last_name'],
                    'email': row['artists.email'],
                    'password': row['artists.password'],
                    'created_at': row['artists.created_at'],
                    'updated_at': row['artists.updated_at'],
                }

                this_artist = user.User(artist_info)
                this_painting.artist = this_artist
                all_purchases.append(this_painting)

        # append to all_paintings list
        
        # print("LENGTH=====",len(all_purchases))
        print("ALL PURCHASES===",all_purchases[0])
        return all_purchases

    # update painting
    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s WHERE id = %(id)s;"

        return connectToMySQL(cls.db_name).query_db(query, data)

    # delete painting
    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # buy painting
    @classmethod
    def buy_painting(cls, data):
        query = "INSERT INTO purchases (user_id, painting_id) VALUES (%(user_id)s, %(painting_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # count purchased paints
    @classmethod
    def count_paintings(cls, data):
        query = "SELECT COUNT(id) AS purchase_count FROM purchases WHERE painting_id = %(id)s;"

        results = connectToMySQL(cls.db_name).query_db(query, data)

        count = results[0]['purchase_count']
        return count




    # static methods
    # validate painting form here
    @staticmethod
    def validate_painting(painting):
        is_valid = True

        if len(painting['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters", "painting")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters", "painting")
        if painting['price'] == "":
            is_valid = False
            flash("Price must be greater than 0", "painting")
        if painting['quantity'] == "":
            is_valid = False
            flash("Quantity must be greater than 0", "painting")

        return is_valid