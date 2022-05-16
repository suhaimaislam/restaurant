from logging import warning
from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import *
from flaskapp.models import *
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from sqlalchemy import desc, func
from itertools import chain

def require_role(role):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.position==role: #<---- changed to position instead of type
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
        highest_rated = Menu.query.order_by(desc(Menu.rating)).limit(3)
        return render_template('index.html', warnings=warnings, highest_rated=highest_rated)
    else:
        top_dishes = Menu.query.order_by(func.random()).limit(3)
        return render_template('index.html', top_dishes=top_dishes)

# home page for admin
@app.route('/admin', methods=['GET'])
@require_role("manager")
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
        address = form.street.data + " " + str(form.apt.data) + " " + form.city.data + " " \
            + form.state.data + " " + str(form.zipcode.data)
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
        orders = Order.query.filter_by(customer_id=current_user.id)
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
                                warnings=warnings,
                                orders=orders)
    elif current_user.is_authenticated and current_user.position=="manager":
        user = Employee.query.filter_by(id=current_user.id).first()
        position = user.position
        salary = user.salary

        return render_template('admin/profile.html',
                                user=user, 
                                position=position,
                                salary=salary,
                                warnings=warnings, 
                                orders=orders)
    elif current_user.is_authenticated and current_user.position=="delivery":
        user = Employee.query.filter_by(id = current_user.id).first()
        position = user.position
        salary = user.salary
        rating = user.rating

        return render_template('employee/delivery_profile.html',
                                user=user, 
                                position=position,
                                salary=salary,
                                warnings=warnings, 
                                orders=orders,
                                rating=rating)

    elif current_user.is_authenticated and current_user.position=="chef":
        user = Employee.query.filter_by(id = current_user.id).first()
        position = user.position
        salary = user.salary
        rating = user.rating

        return render_template('employee/chef_profile.html',
                                user=user, 
                                position=position,
                                salary=salary,
                                warnings=warnings, 
                                orders=orders,
                                rating=rating)

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

# cart page for customers
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if current_user.is_authenticated:
        curr = Customer.query.get(current_user.id)

        cart = curr.dishes
        subtotal = 0
        fee = 0
        total = 0
        for item in cart: # calculate total of cart
            quantity = item.quantity
            subtotal += item.price * quantity
            

        total = subtotal + fee

        form=PlaceOrder()
        if form.validate_on_submit():
            if subtotal < curr.deposit: # places order if order total < customer account deposit

                if curr.status == 'VIP': # 5% discount if customer is VIP
                    subtotal *= 0.95

                

                new_order = Order(total=subtotal, dishes=cart, fees = fee, customer_id=current_user.id, customer_name = current_user.username, status = "open")
                curr.deposit -= subtotal

                cart = curr.dishes
                for item in cart: #reset item quantity to 0 after order is placed
                    item.quantity = 0

                curr.dishes = []
                db.session.add(new_order)
                db.session.commit()
                # print(db.session.query(Order.id, Order.date, Order.total, Order.customer_id, Order.quantity).all())
                
                

                history = 0 # calculate total money spent by customer on all orders
                for order in curr.orders:
                    history += order.total
                
                outstanding = True # check if customer has outstanding complaints
                for complaint in Complaint.query.filter_by(complainee_id=current_user.id):
                    if complaint.type == 'complaint' and complaint.status != 'open':
                        outstanding = False
                    elif complaint.type == 'complaint' and complaint.status == 'open':
                        outstanding = True
                for complaint in Complaint.query.filter_by(filer_id=current_user.id):
                    if complaint.type == 'complaint' and complaint.status != 'open':
                        outstanding = False
                    elif complaint.type == 'complaint' and complaint.status == 'open':
                        outstanding = True
                
                # makes customer status a VIP if customer has placed more than 5 orders
                # and either spent more than $100 or has no outstanding complaints
                if len(curr.orders) > 5 and (history > 100 or outstanding is False):
                    curr.status = "VIP"
                
                db.session.commit()
                # print(db.session.query(Customer.id, Customer.deposit, Customer.status).all())
                return redirect(url_for('profile')) 

            elif subtotal > curr.deposit: # issues warning and does not order if order total > customer account deposit
                new_warning = Warning(content="Order total exceed account deposit", user_id=current_user.id)
                db.session.add(new_warning)
                db.session.commit()
                return redirect(url_for('profile')) 
        return render_template('cart.html', cart=cart, subtotal=subtotal, form=form, fees = fee, total = total)
    else:
        return render_template('cart.html')

# menu page for customers
@app.route('/menu', methods=['GET'])
def menu():
    menudata=Menu.query.filter_by(approved=True)
    all_dishes = [item.serialize() for item in menudata]
    return render_template('menu.html', menus=all_dishes)

# add item from menu page to cart for customers
@app.route('/menu/<int:id>', methods=['GET', 'POST'])
def add_cart(id):
    customer = Customer.query.get(current_user.id)
    dish = Menu.query.get(id)
    form=AddToCart()
    if form.validate_on_submit():
        dish.quantity += 1
        customer.dishes.append(dish)
        db.session.commit()
        return redirect(url_for('cart'))
    return render_template('menu_item.html', form=form, dish=dish)

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
        foodreviews = FoodReview(title=form.title.data, content=form.content.data, \
            rating=form.rating.data, menu_id=form.dish.data, customer_id=current_user.id)
        dish = Menu.query.get(form.dish.data)
        dish.rating = (dish.rating+form.rating.data)/2
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
        complaints = Complaint(content=form.content.data, type=form.type.data, \
            complainee_id=form.complainee.data, filer_id=current_user.id)
        employee = Employee.query.get(form.complainee.data)
        employee.rating = (employee.rating+form.rating.data)/2
        db.session.add(complaints)
        db.session.commit()
        flash('Your review has been created!', 'success')
        return redirect(url_for('discussion'))
    return render_template('create_complaint.html', form=form)

# admin views compliments and complaints
@app.route("/admin/reviews", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_reviews():
    complaintdata = Complaint.query.all()
    return render_template('admin/reviews.html', complaintdata=complaintdata)

    # delivery employee views compliments and complaints
@app.route("/delivery/reviews", methods=['GET', 'POST'])
@login_required
@require_role("delivery")
def delivery_reviews():
    complaintdata = Complaint.query.all()
    return render_template('employee/delivery_reviews.html', complaintdata=complaintdata) 

    # chef employee views compliments and complaints
@app.route("/chef/reviews", methods=['GET', 'POST'])
@login_required
@require_role("chef")
def chef_reviews():
    complaintdata = Complaint.query.all()
    return render_template('employee/chef_reviews.html', complaintdata=complaintdata) 

# admin updates status on compliment and complaints
@app.route("/admin/reviews/<int:id>", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def edit_reviews(id):
    complaint = Complaint.query.get(id)
    if complaint:
        form = UpdateComplaintForm()
        if form.validate_on_submit():
            complaint.status = form.status.data
            db.session.commit()
            if (form.status.data=="warning to complainee"):
                new_warning = Warning(user_id=complaint.complainee_id, content=complaint.content)
                db.session.add(new_warning)
                db.session.commit()
            elif (form.status.data=="warning to filer"):
                new_warning = Warning(user_id=complaint.filer_id, content=complaint.content)
                db.session.add(new_warning)
                db.session.commit()
            return redirect(url_for('reviews'))
    return render_template('admin/update_reviews.html', complaint=complaint, form=form)

# admin view menu
@app.route("/admin/menu", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_menu():
    menudata = Menu.query.all()
    return render_template('admin/menu.html', menudata=menudata)

# chef view menu
@app.route("/employee/menu", methods=['GET', 'POST'])
@login_required
@require_role("chef")
def chef_menu():
    menudata = Menu.query.all()
    return render_template('employee/menu.html', menudata=menudata)


# chef requests new dishes to the menu
@app.route("/admin/menu/add", methods=['GET', 'POST'])
@login_required
@require_role("chef")
def admin_add_menu():
    chefdata = Employee.query.filter_by(position="chef")
    chef_list = [(person.id, person.username) for person in chefdata]
    form = AddMenuForm()
    form.chef.choices=chef_list
    if form.validate_on_submit():
        new_dish = Menu(name=form.name.data, price=form.price.data, \
            description=form.description.data, category=form.category.data, chef_id=form.chef.data)
        db.session.add(new_dish)
        db.session.commit()
        flash('Your dish has been created!', 'success')
        # return redirect(url_for('admin_menu'))
    return render_template('admin/add_menu.html', form=form)


# admin approved new dishes to the menu
@app.route("/admin/menu/<int:id>", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_approve_menu(id):
    dish = Menu.query.get(id)
    form = ApproveMenuForm()
    if form.validate_on_submit():
        if form.approve.data=="Approved":
            dish.approved=True
        else:
            dish.approved=False
        db.session.commit()
        return redirect(url_for('admin_menu'))
    return render_template('admin/approve_menu.html', form=form, dish=dish)

# admin views and manages employees
@app.route("/admin/employees", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_employees():
    employeedata = Employee.query.all()
    for employee in employeedata:
        for item in employee.complaints_filed_against:
            if item.type=="compliment":
                compliments = [(employee.id, item.id)]
    return render_template('admin/employees.html', employeedata=employeedata, compliments=compliments)

# admin adds employee to staff
@app.route("/admin/employees/add", methods=['GET', 'POST'])
@login_required
@require_role("manager")
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

# admin edits employee information
@app.route("/admin/employees/<int:id>", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_update_employee(id):
    employee = Employee.query.get(id)
    form = UpdateEmployeeForm()
    if form.validate_on_submit():
        if form.active.data is True:
            Employee.query.filter_by(id=id).delete()
        else:
            if form.salary.data < employee.salary:
                Warning.query.filter_by(user_id=id).delete()
            employee.position=form.position.data
            employee.salary=form.salary.data
        db.session.commit()
        return redirect(url_for('admin_employees'))
    return render_template('admin/update_employee.html', form=form, employee=employee)

    # admin views and manages orders
@app.route("/admin/orders", methods=['GET', 'POST'])
@login_required
@require_role("manager")
def admin_orders():
    currorders = Order.query.all()
    return render_template('admin/orders.html', currorders=currorders) # make new orders.html file

    # employee views and manages orders
@app.route("/employee/orders", methods=['GET', 'POST'])
@login_required
@require_role("delivery")
def delivery_orders():
    currorders = Order.query.all()
    return render_template('employee/orders.html', currorders=currorders) # make new orders.html file

    # delivery views and manages open delivery orders
    #change this to only include current/unclosed orders
@app.route("/employee/open", methods=['GET', 'POST'])
@login_required
def open_orders():
    currorders = Order.query.all()
    return render_template('employee/deliveries.html', currorders=currorders) # make new orders.html file


    # delivery employees bid on orders
@app.route('/delivery/bid/<int:id>', methods=['GET', 'POST'])
@login_required
def order_bid(id):
    if current_user.is_authenticated and current_user.position=="delivery":
        order = Order.query.get(id)
        form = OrderBidForm()
        if form.validate_on_submit():
            dec_total = float(order.total)
            new_bid = Bids(order_id = order.id,customer_id = order.customer_id, bidder = current_user.id, fee = form.bid.data, customer_name = order.customer_name, new_subtotal = dec_total + form.bid.data, bidder_name = current_user.username)
            db.session.add(new_bid)
            db.session.commit()
            print("THIS WORKED\n\n")
            
            #for loop to test addition of bids
            for item in Bids.query.all():
                cust = Customer.query.get(item.customer_id)
                print(f'{item.id}, order: {item.order_id}, customer: {item.customer_id}, name: {cust.username} bidder: {item.bidder}, fee: {item.fee}')
            flash(f'Your bid of ${form.bid.data} for order #{order.id} is complete!', 'success')
    return render_template('/employee/delivery_bid.html', title='Add Bid', order_bid=order, form = form)

    # admin view current bids
@app.route('/admin/bid/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_bid(id):
    if current_user.is_authenticated and current_user.position=="manager":
        bids = Bids.query.filter_by(order_id = id)
        ord_num = id
        #query returns the fee and id of the lowest bid as a tuple (fee, id)
        minbid = db.session.query(func.min(Bids.fee), Bids.id).filter_by(order_id = id)
        min_val = list(chain(*minbid)) #turns the tuple result into a list 
        #returns the row with the first lowest bidding value
        low = Bids.query.filter_by(id = min_val[1]).first()
        #sets the ranking value to Lowest for display in the Bids table
        low.ranking = "Lowest"
        db.session.commit()
        
    return render_template('/admin/approve_bid.html', title='Add Bid', bids = bids, num = ord_num)

# admin approve lowest bid
@app.route('/admin/select_bid/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_select_bid(id):
    if current_user.is_authenticated and current_user.position=="manager":
        this = id
        bid = Bids.query.filter_by(id = this).first()
        new_fee = bid.fee
        ordernum = bid.order_id
        order = Order.query.get(ordernum)
        order.fees = new_fee
        db.session.commit()
        # return redirect(url_for('admin_orders'))
    return render_template('/admin/bid_selected.html', bids = bid, num = ordernum)