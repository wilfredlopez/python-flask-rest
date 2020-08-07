import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Stores, Store
from datetime import timedelta

app = Flask(__name__)

# CONFIG
app.secret_key = 'WilfredLopez'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')  # ENV VARIABLE OR DEFAULT (data.db)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

api = Api(app)


@app.before_first_request
# Create Tables for Database Automatically
def create_tables():
    db.create_all()

# Creates endpoint to log in. POST: '/auth'
# Accepts {username: '', password: ''}
# @returns
# {
#   "access_token": "eyJ0eXAiOiJKV1..."
# }


jwt = JWT(app, authenticate, identity)


@ app.route('/')
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

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
