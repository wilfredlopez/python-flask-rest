import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        allitems = []
        for row in result:
            allitems.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': allitems}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field is required.')

    @classmethod
    def getItemOrNone(cls, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        item = result.fetchone()
        connection.close()
        return item

    @classmethod
    def insetItem(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item

    @classmethod
    def removeItem(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    @classmethod
    def updateItem(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

  # GET ITEM

    @jwt_required()
    def get(self, name):
        item = Item.getItemOrNone(name)
        return {'item': item}, 200 if item is not None else 404

# CREATE ITEM
    @jwt_required()
    def post(self, name):
        # parser only gets the arguments we specified by adding to parser.
        data = Item.parser.parse_args()
        if Item.getItemOrNone(name) is not None:
            return {'message': f"Item already exist with that name: {name}"}, 400
        item = {'name': name, 'price': data['price']}
        try:
            Item.insetItem(item)
        except:
            return {"Message": "An error occurred inserting item."}, 500
        return {'item': item}, 201


# Delele ITEM

    @jwt_required()
    def delete(self, name):
        item = Item.getItemOrNone(name)
        if item is None:
            return {'message': "Item Not Found"}, 404
        Item.removeItem(name)
        return {'item': item}, 202
# UPDATE ITEM

    @jwt_required()
    def put(self, name):
        # parser only gets the arguments we specified by adding to parser.
        data = Item.parser.parse_args()
        item = Item.getItemOrNone(name)
        uptated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insetItem(uptated_item)
            except:
                return {"message": "An error occurred inserting item."}, 500
            return {'item': uptated_item}, 201
        else:
            try:
                Item.updateItem(uptated_item)
            except:
                return {'message': "An error occurred updating item."}, 500
            return {'item': uptated_item}, 202
