from xmlrpc.client import DateTime
from sqlalchemy import null
import datetime
from app import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # joined = db.Column(db.DateTime, default=datetime.datetime.now())
    position = db.Column(db.String(30), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    ratings = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            # "joined": self.joined,
            "position": self.position,
            "salary": self.salary,
            "ratings": self.ratings
        }


class Customer(db.Model):
    __tablename__ = "customers"
      
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

      
class Visitor(db.Model):
    __tablename__ = "visitors"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    # category
    # image
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "rating": self.rating
        }
    