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
        Employee(id=3, email="aladdin@gmail.com", username="Aladdin", password=bcrypt.generate_password_hash("magiccarpet").decode('utf-8'), type="employee", position="chef", salary=75000),
        Employee(id=6, email="naveen@gmail.com", username="Prince Naveen", password=bcrypt.generate_password_hash("frog").decode('utf-8'), type="employee", position="chef", salary=70000),
    ]

    customer = [
        Customer(id=4, email="twainM@gmail.com", username="Mark Twain", password=bcrypt.generate_password_hash("TomSawyer"), type="customer", status="Registered"),
        Customer(id=5, email="dickensC@yahoo.com", username="Charles Dickens", password=bcrypt.generate_password_hash("2Cities"), type="customer", status="VIP"),
    ]

    menu = [
        Menu(id=1, name='Chocolate Chip Waffles', price=8.5, description='Dough-based, caramelized waffle topped with vanilla bean ice-cream', category='breakfast', chef_id=3, approved=True),
        Menu(id=2, name='Avocado Toast', price=9, description='Sourbread Dough, Tomato, Microgreens', category='breakfast', chef_id=6, approved=True),
        Menu(id=3, name='Peri Peri Chicken Burger', price=12, description='chicken infused with hot chili peppers, jalapenos, lemon, vinegar, herbs, and spices', category='lunch', chef_id=3, approved=True),
        Menu(id=4, name='Fettuccine Alfredo', price=15, description='fresh fettuccine tossed with butter and Parmesan cheese', category='dinner', chef_id=6, approved=True)
    ]

    complaint = [
        Complaint(id=1, content="I want my carpet back", type="complaint", complainee_id=3, filer_id=4),
        Complaint(id=2, content="The best delivery ever", type="compliment", complainee_id=3, filer_id=2),
        Complaint(id=3, content="very rude customer", type="complaint", complainee_id=4, filer_id=2),

        Complaint(id=4, content="I want my carpet back", type="complaint", complainee_id=3, filer_id=4),
        Complaint(id=5, content="The best delivery ever", type="complaint", complainee_id=4, filer_id=2),
        Complaint(id=6, content="very rude customer", type="complaint", complainee_id=2, filer_id=4),
        Complaint(id=7, content="The best delivery ever", type="complaint", complainee_id=4, filer_id=6),
        Complaint(id=8, content="very rude customer", type="complaint", complainee_id=6, filer_id=4)
    ]

    db.session.add_all(menu)
    db.session.add_all(employee)
    db.session.add_all(customer)
    db.session.add_all(complaint)
    db.session.add(test_admin)
    db.session.commit()

    print("Completed!")
    return


if __name__ == '__main__':

    build_sample_db()

    app.run(debug=True)
