from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import FoodReviewForm, RegistrationForm, LoginForm, AddressForm, DepositForm, FoodReviewForm
from flaskapp.models import FoodReview, User, Customer, Employee, Menu
from flask_login import login_user, current_user, logout_user, login_required

menus = [
    {
        'name': 'Chocolate Chip Waffles',
        'price': '8.5',
        'description': 'Dough-based, caramelized waffle topped with vanilla bean ice-cream',
        'category': 'breakfast',
        'rating': '4.3'
    },
    {
        'name': 'Avocado Toast',
        'price': '9',
        'description': 'Sourbread Dough, Tomato, Microgreens',
        'category': 'breakfast',
        'rating': '4.0'
    },
    {
        'name': 'Peri Peri Chicken Burger',
        'price': '12',
        'description': 'chicken infused with hot chili peppers, jalapenos, lemon, vinegar, herbs, and spices',
        'category': 'lunch',
        'rating': '4.6'
    },
    {
        'name': 'Fettuccine Alfredo',
        'price': '15',
        'description': 'fresh fettuccine tossed with butter and Parmesan cheese',
        'category': 'dinner',
        'rating': '4.5'
    }
]

@app.route('/', methods=['GET'])
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        address = form.street.data + " " + str(form.apt.data) + " " + form.city.data + " " + form.state.data + " " + str(form.zipcode.data)
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, address=address)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.type == "customer":
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/employee_login", methods=['GET', 'POST'])
def employee_login():
    if current_user.is_authenticated and current_user.type == "employee":
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('employee_login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
    if current_user.is_authenticated and current_user.type == "customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        status = user.status
        deposit = user.deposit
        address = user.address

        return render_template('profile.html', 
                               title='Customer Profile', 
                               user=user, 
                               status=status,
                               deposit=deposit,
                               address=address)
    elif current_user.is_authenticated and current_user.type == "employee":
        user = Employee.query.filter_by(id=current_user.id).first()
        position = user.position
        salary = user.salary
        return render_template('profile.html', 
                               title='Employee Profile', 
                               user=user, 
                               position=position,
                               salary=salary)
    else:
        flash("You're not allowed to view that page!", 'danger')
        return redirect(url_for('home'))

@app.route('/update_address', methods=['GET', 'POST'])
@login_required
def update_address():
    if current_user.is_authenticated and current_user.type == "customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        form = AddressForm()
        if form.validate_on_submit():
            new_address = form.street.data + " " + str(form.apt.data) + " " + form.city.data + " " + form.state.data + " " + str(form.zipcode.data)
            current_user.address = new_address
            db.session.commit()
            flash('Your address has been updated!', 'success')
            return redirect(url_for('profile'))
    return render_template('update_address.html', title='Update Address', form=form)

@app.route('/deposit_money', methods=['GET', 'POST'])
@login_required
def deposit_money():
    if current_user.is_authenticated and current_user.type == "customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        form = DepositForm()
        if form.validate_on_submit():
            new_deposit= user.deposit + form.deposit.data
            user.deposit = new_deposit
            db.session.commit()
            flash('Your deposit amount has been updated!', 'success')
            return redirect(url_for('profile'))
    return render_template('deposit_money.html', title='Add Deposit', form=form)

@app.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html', menus=menus)

@app.route("/discussion", methods=['GET'])
def discussion():
    food_reviews = FoodReview.query.all()
    return render_template('discussion.html', food_reviews=food_reviews)

@app.route("/discussion/new", methods=['GET', 'POST'])
@login_required
def new_discussion():
    form = FoodReviewForm()
    if form.validate_on_submit():
        review = FoodReview(title=form.title.data, content=form.content.data)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('discussion'))
    return render_template('create_food_review.html', form=form)