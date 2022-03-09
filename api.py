from flask import request, render_template, redirect
from app import app, db
from models import Employees, Customers, Visitors

@app.route('/', methods=['GET'])
def get_home():
    employeeData = Employees.query.all()
    all_employees = [item.serialize() for item in employeeData]
    customerData= Customers.query.all()
    all_customers = [item.serialize() for item in customerData]
    visitorData= Visitors.query.all()
    all_visitors = [item.serialize() for item in visitorData]
    return render_template('index.html', employees=all_employees, customers=all_customers, visitors=all_visitors)
