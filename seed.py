from models import Employees, Customers, Visitors
import datetime

def seed(db):
    employees = [
        Employees(id=1, username="George Washington"),
        Employees(id=2, username="Thomas Jefferson"),
        Employees(id=3, username="Benjamin Franklin"),
        Employees(id=4, username="Abraham Lincoln"),
        Employees(id=5, username="John Adams"),
        Employees(id=6, username="Alexander Hamilton"),
        Employees(id=7, username="Aaron Burr"),
        Employees(id=8, username="James Madison"),
        Employees(id=9, username="James Monroe"),
        Employees(id=10, username="John Jay"),
    ]

    customers = [
        Customers(id=1, username="Mark Twain"),
        Customers(id=2, username="Charles Dickens"),
        Customers(id=3, username="Walt Whitman"),
        Customers(id=4, username="Francis Fitzgerald"),
        Customers(id=5, username="John Steinbeck"),
        Customers(id=6, username="Edgar Allen Poe"),
        Customers(id=7, username="Louisa Alcott"),
        Customers(id=8, username="Agatha Christie"),
        Customers(id=9, username="Jane Austen"),
        Customers(id=10, username="Charlotte Bronte"),
    ]
    
    visitors = [
        Visitors(id=1, username="Brad Pitt"),
        Visitors(id=2, username="Adam Sandler"),
        Visitors(id=3, username="Bradley Cooper"),
        Visitors(id=4, username="Leonardo DiCaprio"),
        Visitors(id=5, username="Tom Hanks"),
        Visitors(id=6, username="Bruce Willis"),
        Visitors(id=7, username="George Clooney"),
        Visitors(id=8, username="Rob Lowe"),
        Visitors(id=9, username="Ben Affleck"),
        Visitors(id=10, username="Alec Baldwin"),
    ]

    db.session.add_all(employees)
    db.session.add_all(customers)
    db.session.add_all(visitors)
    db.session.commit()
