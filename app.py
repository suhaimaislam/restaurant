from flaskapp import app, db, bcrypt
from flaskapp.api import employee_login
from flaskapp.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers
from flask_security import current_user
from flask import render_template, url_for, flash, redirect, request
from flask_security import SQLAlchemyUserDatastore, Security

# Populate a small db with some example entries.
def build_sample_db():

    print("Dropping database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()

    test_admin = Employee(
        id=1, 
        email='admin@gmail.com',
        username='Admin',
        password = bcrypt.generate_password_hash('admin').decode('utf-8'),
        address='admin_address',
        type='employee',
        position='manager',
        salary=100000
    )

    employee = [
        Employee(id=2, email="eugenef@gmail.com", username="Flynn Rider", password=bcrypt.generate_password_hash("letdownyourhair").decode('utf-8'), type="employee", position="delivery", salary=50000),
        Employee(id=7, email="gspeed@gmail.com", username="George Speed", password=bcrypt.generate_password_hash("yellowranger").decode('utf-8'), type="employee", position="delivery", salary=40000),
        Employee(id=3, email="aladdin@gmail.com", username="Aladdin", password=bcrypt.generate_password_hash("magiccarpet").decode('utf-8'), type="employee", position="chef", salary=75000),
        Employee(id=6, email="naveen@gmail.com", username="Prince Naveen", password=bcrypt.generate_password_hash("frog").decode('utf-8'), type="employee", position="chef", salary=70000),
    ]

    customer = [
        Customer(id=4, email="twainM@gmail.com", username="Mark Twain", password=bcrypt.generate_password_hash("TomSawyer"), address = "1000 Test St New York, NY 11111", type="customer", status="Registered"),
        Customer(id=5, email="dickensC@yahoo.com", username="Charles Dickens", password=bcrypt.generate_password_hash("2Cities"), address = "1234 Liberty Ave New York, NY 98765", type="customer", status="VIP"),
    ]

    menu = [
        Menu(id=1, name='Chocolate Chip Waffles', price=8.5, description='Dough-based, caramelized waffle topped with vanilla bean ice-cream', category='breakfast', chef_id=3, approved=True, image="https://res.cloudinary.com/mealthy1/image/upload/ar_16:11,c_fill,f_auto,h_600,q_auto:best,w_800/v1497536871/Peanut-Butter-Chocolate-Chip-Waffles-2-5.jpg"),
        Menu(id=2, name='Avocado Toast', price=9, description='Sourbread Dough, Tomato, Microgreens', category='breakfast', chef_id=6, approved=True, image="https://www.thespruceeats.com/thmb/J6UgyxYr0uZcgPIYmq329LJ8hg8=/3233x2155/filters:fill(auto,1)/avocado-toast-4174244-hero-03-d9d005dc633f44889ba5385fe4ebe633.jpg"),
        Menu(id=3, name='Peri Peri Chicken Burger', price=12, description='chicken infused with hot chili peppers, jalapenos, lemon, vinegar, herbs, and spices', category='lunch', chef_id=3, approved=True, image="https://i.ytimg.com/vi/eGZvxjvJe3c/maxresdefault.jpg"),
        Menu(id=4, name='Fettuccine Alfredo', price=15, description='fresh fettuccine tossed with butter and Parmesan cheese', category='dinner', chef_id=6, approved=True, image="https://food.fnr.sndimg.com/content/dam/images/food/fullset/2011/2/4/1/RX-FNM_030111-Lighten-Up-012_s4x3.jpg.rend.hgtvcom.616.462.suffix/1382539856907.jpeg"),
        Menu(id=5, name='Hard-Shell Chicken Tacos', price=12, description='hard-shell tortilla tacos filled with spiced chicken, cheese, and guac', category='lunch', chef_id=6, approved=True, image='https://images-gmi-pmc.edge-generalmills.com/e59f255c-7498-4b84-9c9d-e578bf5d88fc.jpg')
    ]

    complaint = [
        Complaint(id=1, content="I want my carpet back", type="complaint", complainee_id=3, filer_id=4),
        Complaint(id=2, content="The best delivery ever", type="compliment", complainee_id=3, filer_id=2),
        Complaint(id=3, content="very rude customer", type="complaint", complainee_id=4, filer_id=2),

        Complaint(id=4, content="I want my carpet back", type="complaint", complainee_id=3, filer_id=4),
        Complaint(id=5, content="The best delivery ever", type="compliment", complainee_id=4, filer_id=2),
        Complaint(id=6, content="Showed up late", type="complaint", complainee_id=2, filer_id=4),
        Complaint(id=7, content="The best delivery ever", type="compliment", complainee_id=6, filer_id=4),
        Complaint(id=8, content="very rude customer", type="complaint", complainee_id=4, filer_id=6)
    ]

    # orders = [
    #     Order(id = 1, date = datetime(2022, 5, 14, 15, 36, 26, 863258), total = 26.0, fees = 0, customer_id = 4, status = "open", quantity = None),
    #     Order(id = 2, date = datetime(2022, 5, 14, 15, 36, 46, 544075), total = 54.0, fees = 0, customer_id = 4, status = "open", quantity = None),
    #     Order(id = 3, date = datetime(2022, 5, 14, 15, 36, 51, 446025), total = 9.0, fees = 0, customer_id= 4, status = "open", quantity = None),
    #     Order(id = 4, date = datetime(2022, 5, 14, 15, 37, 21, 421083), total = 34.0, fees = 0, customer_id = 4, status = "open", quantity = None),
    #     Order(id = 5, date = datetime(2022, 5, 14, 15, 39, 13, 193241), total = 42.75, fees = 0,customer_id = 5, status = "open", quantity = None),
    #     Order(id = 6, date = datetime(2022, 5, 14, 15, 39, 18, 94277), total = 8.075, fees = 0, customer_id = 5, status = "open", quantity = None)
    # ]

    db.session.add_all(menu)
    db.session.add_all(employee)
    db.session.add_all(customer)
    db.session.add_all(complaint)
    db.session.add(test_admin)
    # db.session.add_all(orders)
    db.session.commit()

    print("Completed!")
    return


if __name__ == '__main__':

    build_sample_db()

    app.run(debug=True)
