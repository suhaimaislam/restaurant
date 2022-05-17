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

    # Relationships
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
    rating = db.Column(db.Float, default=5.0)
    demotion = db.Column(db.Integer, default=0)
    promotion = db.Column(db.Integer, default=0)

    # Relationships
    dishes = db.relationship('Menu', back_populates='chef', lazy='dynamic') # dishes made by chef
    orders = db.relationship('Order', back_populates='delivery_person') # orders delivered by delivery person
    bids = db.relationship('Bids', back_populates='employees')

    __mapper_args__ = {'polymorphic_identity': 'employee'}

    def __repr__(self):
        return f'Employee({self.username}, {self.email}, {self.position}, {self.salary})'

# customer model (subclass of user)
class Customer(User):
    __tablename__ = "customers"
      
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(30), default="Registered")
    deposit = db.Column(db.Float, default=0.0)
    close_account = db.Column(db.Boolean, default=False)

    # Relationships
    dishes = db.relationship('Menu', back_populates='customer', lazy='dynamic') # dishes in cart
    foodreviews = db.relationship('FoodReview', back_populates='author', lazy='dynamic')
    orders = db.relationship('Order', back_populates='customer')
    order_bids = db.relationship('Bids', back_populates='customer')

    __mapper_args__ = {'polymorphic_identity': 'customer'}

    def __repr__(self):
        return f'Customer({self.username}, {self.email}, {self.status}, {self.deposit}, {self.close_account})'

# blacklist model (for users kicked out of system)
class Blacklist(db.Model, UserMixin):
    __tablename__ = "blacklists"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    date_blacklisted = db.Column(db.DateTime, nullable=False,  default=datetime.now)

    def __repr__(self):
        return f'Blacklist({self.email})'
    
# menu model
class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    rating = db.Column(db.Float, nullable=False, default=5.0)
    approved = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Integer, default = 0)
    counter = db.Column(db.Integer, default=0) # number of items dish was ordered 

    # Relationships
    reviews = db.relationship('FoodReview', back_populates='dish', lazy='dynamic')
    image = db.Column(db.String(500), nullable=True)

    chef_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    chef = db.relationship('Employee', back_populates='dishes')

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', back_populates='dishes')

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('Order', back_populates='dishes')

    def __repr__(self):
        return f"Menu('{self.name}', '{self.price}', '{self.description}', '{self.category}', '{self.rating}', '{self.image}')"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "rating": self.rating,
            "chef": self.chef,
            "approved": self.approved,
            "image": self.image
        }

# food review model
class FoodReview(db.Model):
    __tablename__ = 'food_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,  default=datetime.now) #<---changed from UTC to Local Time
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    
    #Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    author = db.relationship('Customer', back_populates='foodreviews')

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    dish = db.relationship('Menu', back_populates='reviews')

    def __repr__(self):
        return f"FoodReview('{self.title}', '{self.date_posted}')"

# complaints model
class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_filed = db.Column(db.DateTime, nullable=False, default=datetime.now)
    type = db.Column(db.String, default="compliment")
    # add date updated
    complainee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String, nullable=False, default="open")

    #Relationships
    complainee = db.relationship('User', foreign_keys='Complaint.complainee_id', back_populates='complaints_filed_against')
    filer = db.relationship('User', foreign_keys='Complaint.filer_id', back_populates='complaints_filed')


    def __repr__(self):
        return f'Complaint({self.content}, {self.date_filed}, {self.complainee_id}, {self.filer_id}, {self.complainee}, {self.filer}, {self.status})'
    
# warnings model
class Warning(db.Model):
    __tablename__ = "warnings"

    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)    

    #Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='warnings')

    def __repr__(self):
        return f'Warning({self.date_received}, {self.content}, {self.user_id})'

# orders model
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total = db.Column(db.Float, default = 0.0)
    fees = db.Column(db.Float, default = 0.0)
    status = db.Column(db.String(30), default="open")
    # quantity = db.Column(db.Integer)
    delivery_type = db.Column(db.String(20), nullable=False)

    #Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')

    delivery_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    delivery_person = db.relationship('Employee', back_populates='orders')

    dishes = db.relationship('Menu', back_populates='order', lazy='dynamic')
    bids = db.relationship('Bids', back_populates='orders', lazy='dynamic')

    def __repr__(self):
        return f'Warning({self.date}, {self.total}, {self.dishes}, {self.customer_id}, {self.delivery_type})'

class Bids(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    bidder = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    bidder_name = db.Column(db.String(30))
    fee = db.Column(db.Float, default = 0.00)
    customer_name = db.Column(db.String(30))
    new_subtotal = db.Column(db.Float, default = 0.0)
    ranking = db.Column(db.String(30), default = " ")

    # Relationships
    customer = db.relationship('Customer', back_populates='order_bids')
    orders = db.relationship('Order', back_populates='bids')
    employees = db.relationship('Employee', back_populates='bids')