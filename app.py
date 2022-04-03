from flaskapp import app, db
from flaskapp.models import *


if __name__ == '__main__':
    print("Dropping database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()

    menu = [
        Menu(id=1, name='Chocolate Chip Waffles', price=8.5, description='Dough-based, caramelized waffle topped with vanilla bean ice-cream', category='breakfast'),
        Menu(id=2, name='Avocado Toast', price=9, description='Sourbread Dough, Tomato, Microgreens', category='breakfast'),
        Menu(id=3, name='Peri Peri Chicken Burger', price=12, description='chicken infused with hot chili peppers, jalapenos, lemon, vinegar, herbs, and spices', category='lunch'),
        Menu(id=4, name='Fettuccine Alfredo', price=15, description='fresh fettuccine tossed with butter and Parmesan cheese', category='dinner')
    ]
    db.session.add_all(menu)
    db.session.commit()

    print("Completed!")
    app.run(debug=True)
