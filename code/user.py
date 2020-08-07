import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_user_by_name = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(select_user_by_name, (username,))
        row = result.fetchone()
        user = None
        if row:
            user = cls(*row)  # create new user User(*row)
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, userId: int):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_user_by_name = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(select_user_by_name, (userId,))
        row = result.fetchone()
        user = None
        if row:
            user = cls(*row)  # create new user User(*row)
        connection.close()
        return user


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='This field is required.')
        parser.add_argument('password', type=str, required=True,
                            help='This field is required.')
        data = parser.parse_args()
        if User.find_by_username(data['username']) is None:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'INSERT INTO users VALUES (NULL, ?, ?)'
            cursor.execute(query, (data['username'], data['password']))
            connection.commit()
            connection.close()
            return {"message": "User Created Succesfully"}, 201
        return {'message': "User already exist"}, 400
