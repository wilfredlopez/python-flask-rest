import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required


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


class User(Resource):
    @jwt_required()
    def get(Cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message': 'User Not Found.'}, 404
        return {'user': user.json()}, 200

    @jwt_required()
    def delete(Cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message': None}, 404
        else:
            user.delete()
        return {"message": "User Deleted."}
