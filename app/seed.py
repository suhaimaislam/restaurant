# from unicodedata import name
from models import Employee, Customer, Visitor, Menu

def seed(db):
    employees = [
        Employee(id=1, name="Flynn Rider", username="EugeneF", password="letdownyourhair", position="Delivery", salary=70000, ratings=2.4),
        Employee(id=2, name="Levi Ackerman", username="LeviA", password="fidgetspinner", position="Chef", salary=100000, ratings=5),
        Employee(id=3, name="Annabeth Chase", username="WiseGirl", password="ih8spiders", position="Manager", salary=90000, ratings=5),
        Employee(id=4, name="Osamu Dazai", username="ODasaku", password="2xsuicide", position="Delivery", salary=84000, ratings=3.2),
        Employee(id=5, name="Kaz Brekker", username="Rietveld6", password="noMourners", position="Chef", salary=120000, ratings=5),
    ]

    customers = [
        Customer(id=1, name="Mark Twain"),
        Customer(id=2, name="Charles Dickens"),
        Customer(id=3, name="Walt Whitman"),
        Customer(id=4, name="Francis Fitzgerald"),
        Customer(id=5, name="John Steinbeck"),
    ]
    
    visitors = [
        Visitor(id=1, name="Brad Pitt"),
        Visitor(id=2, name="Adam Sandler"),
        Visitor(id=3, name="Bradley Cooper"),
        Visitor(id=4, name="Leonardo DiCaprio"),
        Visitor(id=5, name="Tom Hanks"),
    ]

    menus = [
        Menu(id=1, name="Waffles", price=8.5, description="Dough-based, caramelized waffle topped with vanilla bean ice-cream", rating=4.3),
        Menu(id=2, name="Veggie Omelette", price=6, description="Mushrooms, Onions, Peppers", rating=4),
        Menu(id=3, name="Oatmeal", price=7.25, description="Cinnamon, Honey, Blueberries", rating=3.7),
        Menu(id=4, name="Chocolate-Chip Pancakes", price=9, description="Maple Syrup, Strawberries", rating=5),
        Menu(id=5, name="Avocado Toast", price=9.5, description="Sourbread Dough, Tomato, Microgreens", rating=4.6),
    ]

    db.session.add_all(employees)
    db.session.add_all(customers)
    db.session.add_all(visitors)
    db.session.add_all(menus)
    db.session.commit()
