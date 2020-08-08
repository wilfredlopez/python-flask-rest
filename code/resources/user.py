import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required, get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from werkzeug.security import safe_str_cmp
from blacklist import BLACK_LIST

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
        ### MAKE SURE IS ADMIN USER ###
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {
                'message': "Admin privilege required."
            }
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


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            'access_token': new_token
        }


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACK_LIST.add(jti)
        return {
            'message': "Successfully logged out."
        }
