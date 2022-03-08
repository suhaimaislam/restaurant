from models import Employees, Customers, Visitors
import datetime

def seed(db):
    employees = [

    ]

    customers = [

    ]
    
    visitors = [

    ]

    db.session.add_all(employees)
    db.session.add_all(customers)
    db.session.add_all(visitors)
    db.session.commit()
