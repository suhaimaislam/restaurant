from flaskapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql.schema import ForeignKey

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), default="customer")
    address = db.Column(db.Text(30))

    def __repr__(self):
        return f'User({self.username}, {self.email},)'


class Employee(User):
    __tablename__ = "employees"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    position = db.Column(db.String(50))
    salary = db.Column(db.Float)

    def __repr__(self):
        return f'Employee({self.username}, {self.email}, {self.position}, {self.salary})'


class Customer(User):
    __tablename__ = "customers"
      
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(30), default="Registered")
    deposit = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'Employee({self.username}, {self.email}, {self.status}, {self.deposit})'
    

class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    # category
    # image
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "ratings": self.ratings
        }

class FoodReview(db.Model):
    __tablename__ = 'food_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # def __repr__(self):
    #     return f'FoodReview({self.menu}, {self.customer})'