from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, Items


app = Flask(__name__)
app.secret_key = 'WilfredLopez'
api = Api(app)

# Creates endpoint to log in. POST: '/auth'
# Accepts {username: '', password: ''}
# @returns
# {
#   "access_token": "eyJ0eXAiOiJKV1..."
# }
jwt = JWT(app, authenticate, identity)


@app.route('/')
def home():
    return render_template('index.html')


# Inherit from Resource


# Adding resouces to API
# localhost:5000/items
# localhost:5000/item/name
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
