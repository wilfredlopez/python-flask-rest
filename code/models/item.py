import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    price = Column(Float(precision=2))
    store_id = Column(Integer, ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: int, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_name(cls, name: str):
        item = None
        try:
            item = cls.query.filter_by(name=name).first()
        except:
            print('there was an error')
        if item is None:
            return None
        return item

    @classmethod
    def getAll(cls):
        # data = list(map(lambda x: x.json(), cls.query.all()))
        data = [x.json() for x in cls.query.all()]
        return data
