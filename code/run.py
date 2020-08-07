from app import app
from db import db


@app.before_first_request
# Create Tables for Database Automatically
def create_tables():
    db.create_all()


db.init_app(app)
