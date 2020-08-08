import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy import Column, String, Integer, Float
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self):
        return {id: self.id, 'name': self.name, 'items': [i.json() for i in self.items.all()]}

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
        store = None
        try:
            store = cls.query.filter_by(name=name).first()
        except:
            print('there was an error')
        if store is None:
            return None
        return store

    @classmethod
    def getAll(cls):
        # data = list(map(lambda x: x.json(), cls.query.all()))
        data = [x.json() for x in cls.query.all()]
        return data
