import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Stores(Resource):
    def get(self):
        stores = StoreModel.getAll()
        return {'stores': stores}


class Store(Resource):

  # GET Store

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'store': None}, 404
        return {'store': store.json()}, 200

# CREATE Store
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name) is not None:
            return {'message': f"Store already exist with that name: {name}"}, 400
        store = StoreModel(name)
        try:
            store.save()
        except:
            return {"Message": "An error occurred inserting store."}, 500
        return {'store': store.json()}, 201


# Delele Store


    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': "store Not Found"}, 404
        store.delete()
        return {'store': store.json()}, 202
