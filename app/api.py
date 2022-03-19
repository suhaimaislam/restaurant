from flask import request, render_template, redirect, jsonify
from app import app, db
from models import Employee, Customer, Visitor, Menu

@app.route('/', methods=['GET'])
def get_home():
    employeeData = Employee.query.all()
    all_employees = [item.serialize() for item in employeeData]
    customerData= Customer.query.all()
    all_customers = [item.serialize() for item in customerData]
    visitorData= Visitor.query.all()
    all_visitors = [item.serialize() for item in visitorData]
    menuData= Menu.query.all()
    all_menus = [item.serialize() for item in menuData]
    return render_template('index.html', employees=all_employees, customers=all_customers, visitors=all_visitors, menus=all_menus)

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/menu', methods=['GET'])
def get_menu():
    menuData= Menu.query.all()
    all_menus = [item.serialize() for item in menuData]
    return render_template('menu.html', menus=all_menus)

