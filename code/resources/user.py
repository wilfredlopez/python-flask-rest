import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    def get(self):
        return UserModel.getAll()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='This field is required.')
        parser.add_argument('password', type=str, required=True,
                            help='This field is required.')
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']) is None:
            user = UserModel(None, data['username'], data['password'])
            user.save()
            return {"message": "User Created Succesfully"}, 201
        return {'message': "User already exist"}, 400
