import os
from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, Items
from resources.store import Stores, Store
from datetime import timedelta
from blacklist import BLACK_LIST

app = Flask(__name__)

# CONFIG
app.secret_key = 'WilfredLopez'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')  # ENV VARIABLE OR DEFAULT (data.db)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=3)

api = Api(app)


@app.before_first_request
# Create Tables for Database Automatically
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(user_id):
    if user_id == 1:  # Instead of hardcoding you should read from config or database.
        return {
            'is_admin': True
        }
    return {
        'is_admin': False
    }


@jwt.token_in_blacklist_loader
def check_if_id_in_blacklist(decripted_token):
    return decripted_token['jti'] in BLACK_LIST


@jwt.expired_token_loader
def expire_token_callback():
    return jsonify({
        'description': "access token has expired.",
        'error': "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'description': "Signiture verification failed.",
        'error': "invalid_token"
    }), 401


@jwt.unauthorized_loader
def not_authorized_request_callback():
    return jsonify({
        'description': "Request does not contain an access token. please send Bearer token",
        'error': "authorization_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token_loader_callback():
    return jsonify({
        'description': "The token has expired.",
        'error': "token_revoked"
    }), 401


@app.route('/')
def home():
    return render_template('index.html')


# Inherit from Resource


# Adding resouces to API
# localhost:5000/items
# localhost:5000/item/name
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
