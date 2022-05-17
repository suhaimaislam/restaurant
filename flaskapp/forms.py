from cgi import print_exception
from email.policy import default
from tokenize import String
from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskapp.models import *

# form for visitor to register as customer
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    street = StringField('Mailing Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        blacklisted = Blacklist.query.filter_by(email=email.data).first()
        if blacklisted:
            raise ValidationError('Unable to register. Your email has been blacklisted.')

# form for user to login
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# form for customer to quit the system
class QuitForm(FlaskForm):
    quit = BooleanField('Delete Account')
    submit = SubmitField('Delete')

# form for user to change address
class AddressForm(FlaskForm):
    street = StringField('Mailing Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    submit = SubmitField('Update')

# form for customer to deposit money 
class DepositForm(FlaskForm):
    deposit = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

# form for customer to submit food review
class FoodReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    dish = SelectField('Dish', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    rating = SelectField('Rating', coerce=int, choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    submit = SubmitField('Post')

# form for user to file a compliment/complaint
class ComplaintForm(FlaskForm):
    complainee = SelectField('About', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    type=SelectField('Review Type', choices = [('0', '-- select an option --'), ('compliment', 'compliment'), ('complaint', 'complaint')])
    rating = SelectField('Rating', coerce=int, choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[DataRequired()])
    submit = SubmitField('Post')

# form for manager to update compliment/complaint status
class UpdateComplaintForm(FlaskForm):
    status = SelectField('Status', \
        choices = [('0', '-- select an option --'), ('open', 'open'), \
            ('warning to filer', 'warning to filer'), ('warning to complainee', 'warning to complainee')])
    submit = SubmitField('Save')

# form for chef to request dish to the menu
class AddMenuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = StringField('Image Link', validators=[DataRequired()])
    category = SelectField('Category', choices = [('0', '-- select an option --'), ('breakfast', 'breakfast'), ('lunch', 'lunch'), ('dinner', 'dinner')], validators=[DataRequired()])
    chef = SelectField('Chef', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')

# form for manager to approve a request for a new dish
class ApproveMenuForm(FlaskForm):
    approve = SelectField('Category', choices = [('0', '-- select an option --'), ('Approved', 'Approved'), ('Denied', 'Denied')], validators=[DataRequired()])
    submit = SubmitField('Add')

# form for manager to hire employees and add them to employee list
class AddEmployeeForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    position = SelectField('Position', choices = [('0', '-- select an option --'), ('manager', 'manager'), ('chef', 'chef'), ('delivery', 'delivery')], validators=[DataRequired()])
    salary = FloatField('Salary', validators=[DataRequired()])
    submit = SubmitField('Add')

# form for manager to update employee information
class UpdateEmployeeForm(FlaskForm):
    position = SelectField('Position', choices = [('0', '-- select an option --'), ('manager', 'manager'), ('chef', 'chef'), ('delivery', 'delivery')], validators=[DataRequired()])
    salary = FloatField('Salary')
    active = BooleanField('Fire Employee')
    submit = SubmitField('Update')

# form for manager to update customer information
class UpdateCustomerForm(FlaskForm):
    active = BooleanField('Blacklist Customer')
    submit = SubmitField('Update')

# form to add to cart
class AddToCart(FlaskForm):
    quantity = SelectField('Quantity', coerce=int, choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6,6), (7,7), (8,8), (9,9), (10,10)])
    submit = SubmitField('Add To Cart')

# form to proceed to checkout
class Checkout(FlaskForm):
    delivery_type = SelectField('Delivery Options', choices=[('0', '-- select an option --'), ('Pickup in-person', 'Pickup in-person'), ('Deliver to address', 'Deliver to address')], validators=[DataRequired()])
    submit = SubmitField('Checkout')

# form to place order
class PlaceOrder(FlaskForm):
    submit = SubmitField('Place Order')

# form to place order for delivery
# class PlaceDelivery(FlaskForm):
#     submit = SubmitField('Delivery')

# form for delivery bidding
class OrderBidForm(FlaskForm):
    bid = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')