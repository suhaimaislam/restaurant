from logging import warning
from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import *
from flaskapp.models import *
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps

def require_role(role):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.type==role:
                return redirect("/")
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator

# home page for customers
@app.route('/', methods=['GET'])
@app.route("/home")
def home():
    if current_user.is_authenticated:
        warnings = Warning.query.filter_by(user_id=current_user.id)
        return render_template('index.html', warnings=warnings)
    else:
        return render_template('index.html')

# home page for employees
@app.route('/admin', methods=['GET'])
@require_role("employee")
def admin_home():
    return render_template('admin/home.html')

# signup page for visitors
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

# login page for customers
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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

# login page for employees
@app.route("/employee_login", methods=['GET', 'POST'])
def employee_login():
    if current_user.is_authenticated:
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

# logout page 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# profile page for employees and customers
@app.route("/profile")
@login_required
def profile():
    if current_user.is_authenticated:
        warnings = Warning.query.filter_by(user_id=current_user.id)
    if current_user.is_authenticated and current_user.type=="customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        status = user.status
        deposit = user.deposit
        address = user.address

        return render_template('profile.html', 
                                user=user, 
                                status=status,
                                deposit=deposit,
                                address=address,
                                warnings=warnings)
    elif current_user.is_authenticated and current_user.type=="employee":
        user = Employee.query.filter_by(id=current_user.id).first()
        position = user.position
        salary = user.salary

        return render_template('admin/profile.html', 
                                user=user, 
                                position=position,
                                salary=salary,
                                warnings=warnings)

# update address page for customers
@app.route('/update_address', methods=['GET', 'POST'])
@login_required
def update_address():
    if current_user.is_authenticated and current_user.type=="customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        form = AddressForm()
        if form.validate_on_submit():
            new_address = form.street.data + " " + str(form.apt.data) + " " + form.city.data + " " + form.state.data + " " + str(form.zipcode.data)
            current_user.address = new_address
            db.session.commit()
            flash('Your address has been updated!', 'success') 
            ##return redirect(url_for('profile')) #cancelling redirection to see flash confirm message
    return render_template('update_address.html', title='Update Address', form=form)

# deposit money page for customers
@app.route('/deposit_money', methods=['GET', 'POST'])
@login_required
def deposit_money():
    if current_user.is_authenticated and current_user.type=="customer":
        user = Customer.query.filter_by(id=current_user.id).first()
        form = DepositForm()
        if form.validate_on_submit():
            new_deposit= user.deposit + form.deposit.data
            user.deposit = new_deposit
            db.session.commit()
            flash('Your deposit amount has been updated!', 'success')
            ##return redirect(url_for('profile')) #cancelling redirection to see flash confirm message
    return render_template('deposit_money.html', title='Add Deposit', form=form)

# menu page for customers
@app.route('/menu', methods=['GET'])
def menu():
    menudata=Menu.query.all()
    all_dishes = [item.serialize() for item in menudata]
    return render_template('menu.html', menus=all_dishes)

# discussion page for customers
@app.route("/discussion", methods=['GET'])
def discussion():
    food_reviews = FoodReview.query.all()
    complaints = Complaint.query.all()
    return render_template('discussion.html', food_reviews=food_reviews, complaints=complaints)

# add new food review page for customers
@app.route("/discussion/new_food_review", methods=['GET', 'POST'])
@login_required
def new_food_review():
    menudata=Menu.query.all()
    menu_list=[(item.id, item.name) for item in menudata]
    form = FoodReviewForm()
    form.dish.choices=menu_list
    if form.validate_on_submit():
        foodreviews = FoodReview(title=form.title.data, content=form.content.data, menu_id=form.dish.data, customer_id=current_user.id)
        db.session.add(foodreviews)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('discussion'))
    return render_template('create_food_review.html', form=form)

# add new employee review page for customers
@app.route("/discussion/new_employee_review", methods=['GET', 'POST'])
@login_required
def new_employee_review():
    employeedata=Employee.query.all()
    employee_list=[(person.id, person.username) for person in employeedata]
    form = ComplaintForm()
    form.complainee.choices=employee_list
    if form.validate_on_submit():
        complaints = Complaint(content=form.content.data, complainee_id=form.complainee.data, filer_id=current_user.id)
        db.session.add(complaints)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('discussion'))
    return render_template('create_complaint.html', form=form)

# admin views compliments and complaints
@app.route("/admin/reviews", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def reviews():
    complaintdata = Complaint.query.all()
    return render_template('admin/reviews.html', complaintdata=complaintdata) 

# admin updates status on compliment and complaints
@app.route("/admin/reviews/<int:id>", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def edit_reviews(id):
    complaint = Complaint.query.get(id)
    if complaint:
        form = UpdateComplaintForm()
        if form.validate_on_submit():
            complaint.status = form.status.data
            db.session.commit()
            if (form.status.data=="issue warning"):
                new_warning = Warning(user_id=complaint.complainee_id, content=complaint.content)
                db.session.add(new_warning)
                db.session.commit()
            return redirect(url_for('reviews'))
    return render_template('admin/update_reviews.html', complaint=complaint, form=form) 

# admin and chef view menu
@app.route("/admin/menu", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def admin_menu():
    menudata = Menu.query.all()
    return render_template('admin/menu.html', menudata=menudata)

# admin and chef add new dishes to the menu
@app.route("/admin/menu/add", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def admin_add_menu():
    chefdata = Employee.query.filter_by(position="chef")
    chef_list = [(person.id, person.username) for person in chefdata]
    form = AddMenuForm()
    form.chef.choices=chef_list
    if form.validate_on_submit():
        new_dish = Menu(name=form.name.data, price=form.price.data, description=form.description.data, category=form.category.data, chef_id=form.chef.data)
        db.session.add(new_dish)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('admin_menu'))
    return render_template('admin/add_menu.html', form=form)

# admin views and manages employees
@app.route("/admin/employees", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def admin_employees():
    employeedata = Employee.query.all()
    return render_template('admin/employees.html', employeedata=employeedata)

# admin and chef add new dishes to the menu
@app.route("/admin/employees/add", methods=['GET', 'POST'])
@login_required
@require_role("employee")
def admin_add_employee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(email=form.name.data + "@gmail.com", username=form.name.data, \
            password=bcrypt.generate_password_hash('resetpassword').decode('utf-8'), address="N/A", \
                type="employee", position=form.position.data, salary=form.salary.data)
        db.session.add(new_employee)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('admin_employees'))
    return render_template('admin/add_employee.html', form=form)
