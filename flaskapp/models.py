from flaskapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_security import RoleMixin

# load current_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text(30))
    type = db.Column(db.String(30))

    complaints_filed_against = db.relationship('Complaint', foreign_keys='Complaint.complainee_id', back_populates='complainee')
    complaints_filed = db.relationship('Complaint', foreign_keys='Complaint.filer_id', back_populates='filer')

    warnings = db.relationship('Warning', back_populates='user')

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'user'
    }              

    def __repr__(self):
        return f'User({self.username}, {self.email},)'

# employee model (subclass of user)
class Employee(User):
    __tablename__ = "employees"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    position = db.Column(db.String(50))
    salary = db.Column(db.Float)
    dishes = db.relationship('Menu', back_populates='chef', lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'employee'}

    def __repr__(self):
        return f'Employee({self.username}, {self.email}, {self.position}, {self.salary})'

# customer model (subclass of user)
class Customer(User):
    __tablename__ = "customers"
      
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(30), default="Registered")
    deposit = db.Column(db.Float, default=0.0)
    foodreviews = db.relationship('FoodReview', back_populates='author', lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'customer'}

    def __repr__(self):
        return f'Employee({self.username}, {self.email}, {self.status}, {self.deposit})'
    
# menu model
class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    reviews = db.relationship('FoodReview', back_populates='dish', lazy='dynamic')
    chef_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    chef = db.relationship('Employee', back_populates='dishes')
    # image

    def __repr__(self):
        return f"Menu('{self.name}', '{self.price}', '{self.description}', '{self.category}')"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category
        }

# food review model
class FoodReview(db.Model):
    __tablename__ = 'food_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    author = db.relationship('Customer', back_populates='foodreviews')

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    dish = db.relationship('Menu', back_populates='reviews')

    def __repr__(self):
        return f"FoodReview('{self.title}', '{self.date_posted}')"

# complaints model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_filed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # add date updated
    complainee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    complainee = db.relationship('User', foreign_keys='Complaint.complainee_id', back_populates='complaints_filed_against')
    filer = db.relationship('User', foreign_keys='Complaint.filer_id', back_populates='complaints_filed')

    status = db.Column(db.String, nullable=False, default="open")

    def __repr__(self):
        return f'Complaint({self.content}, {self.date_filed}, {self.complainee_id}, {self.filer_id}, {self.complainee}, {self.filer}, {self.status})'
    
# warnings model
class Warning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)    

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='warnings')

    def __repr__(self):
        return f'Warning({self.date_received}, {self.content}, {self.user_id})'