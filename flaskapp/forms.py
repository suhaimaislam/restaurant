from cgi import print_exception
from tokenize import String
from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskapp.models import User

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
    apt = IntegerField('Apt/Suite/Floor', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# form for user to login
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# form for user to change address
class AddressForm(FlaskForm):
    street = StringField('Mailing Address', validators=[DataRequired()])
    apt = IntegerField('Apt/Suite/Floor', validators=[DataRequired()])
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
    submit = SubmitField('Post')

# form for user to file a compliment/complaint
class ComplaintForm(FlaskForm):
    complainee = SelectField('About', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

# form for manager to update compliment/complaint status
class UpdateComplaintForm(FlaskForm):
    status = SelectField('Status', choices = [('open', 'open'), ('dismiss', 'dismiss'), ('issue warning', 'issue warning')])
    submit = SubmitField('Save')

# form for manager and chef to add dishes to the menu
class AddMenuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices = [('breakfast', 'breakfast'), ('lunch', 'lunch'), ('dinner', 'dinner')])
    chef = SelectField('Chef', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')

# form for manager to hire employees and add them to employee list
class AddEmployeeForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    position = SelectField('Position', choices = [('manager', 'manager'), ('chef', 'chef'), ('delivery', 'delivery')])
    salary = FloatField('Salary', validators=[DataRequired()])
    submit = SubmitField('Add')