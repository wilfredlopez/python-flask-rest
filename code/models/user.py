import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def getAll(cls):
        data = list(map(lambda x: x.json(), cls.query.all()))
        return data

    def json(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username: str):
        user = None
        try:
            user = cls.query.filter_by(username=username).first()
        except:
            print('there was an error finding user.')
        if user is None:
            return None
        return user

    @classmethod
    def find_by_id(cls, userId: int):
        user = None
        try:
            user = cls.query.filter_by(id=userId).first()
        except:
            print('there was an error finding user.')
        if user is None:
            return None
        return user
