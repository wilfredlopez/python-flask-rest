import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import safe_str_cmp

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True,
                          help='This field is required.')
_user_parser.add_argument('password', type=str, required=True,
                          help='Every user needs a password.')


class UserRegister(Resource):
    def get(self):
        return UserModel.getAll()

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']) is None:
            user = UserModel(None, data['username'], data['password'])
            user.save()
            return {"message": "User Created Succesfully"}, 201
        return {'message': "User already exist"}, 400


class User(Resource):
    @jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message': 'User Not Found.'}, 404
        return {'user': user.json()}, 200

    @jwt_required
    def delete(Cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message': None}, 404
        else:
            user.delete()
        return {"message": "User Deleted."}


class UserLogin(Resource):

    # LOGIN USER
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        return {
            "message": "invalid credentials"
        }, 401
