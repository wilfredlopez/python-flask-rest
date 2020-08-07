import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    def get(self):
        allitems = ItemModel.getAll()
        return {'items': allitems}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field is required.')
    parser.add_argument('store_id', type=int, required=True,
                        help='Every item needs a store id.')
  # GET ITEM

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'item': None}, 404
        return {'item': item.json()}, 200

# CREATE ITEM
    @jwt_required()
    def post(self, name):
        # parser only gets the arguments we specified by adding to parser.
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name) is not None:
            return {'message': f"Item already exist with that name: {name}"}, 400
        # {'name': name, 'price': data['price']}
        item = ItemModel(name, **data)
        try:
            item.save()
        except:
            return {"Message": "An error occurred inserting item."}, 500
        return {'item': item.json()}, 201


# Delele ITEM


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': "Item Not Found"}, 404
        item.delete()
        return {'item': item.json()}, 202
# UPDATE ITEM

    @jwt_required()
    def put(self, name):
        # parser only gets the arguments we specified by adding to parser.
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # {'name': name, 'price': data['price']}
        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occurred inserting item."}, 500
        else:
            try:
                item.price = data['price']
                item.save()
            except:
                return {'message': "An error occurred updating item."}, 500
        return {'item': item.json()}, 202
