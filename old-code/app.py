from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': "austria",
        'items': [
            {'name': 'item 1', 'price': 15.99}
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


def createSingleStoreItem(data):
    item = {'name': data['name'], 'price': data['price']}
    return item


def createSingleStore(data):
    new_store = {
        'name': data['name'],
        'items': []
    }
    return new_store


@app.route('/stores', methods=["POST"])
# Post /store data: {name:}
def create_store():
    data = request.get_json()
    new_store = createSingleStore(data)
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/stores/<string:name>/item', methods=["POST"])
# POST /store/<string:name>/item {name:, price:}
def create_item_in_store(name: str):
    data = request.get_json()
    for store in stores:
        if(store['name'] == name):
            item = createSingleStoreItem(data)
            store['items'].append(item)
            return jsonify({'item': item})
    return jsonify({'message': "Store Not Found"})


@app.route('/stores')
# GET /store
def get_stores():
    return jsonify({'stores': stores})


@app.route('/stores/<string:name>')
# GET /store/<string:name>
def get_store_by_name(name: str):
    for store in stores:
        if(store['name'] == name):
            return jsonify({'store': store})
    return jsonify({'message': "Store Not Found"})


@app.route('/stores/<string:name>/items')
# GET /store/<string:name>/item
def get_items_in_store(name: str):
    for store in stores:
        if(store['name'] == name):
            return jsonify({'items': store['items']})
    return jsonify({'message': "Store Not Found"})


app.run(port=5000, debug=True)
