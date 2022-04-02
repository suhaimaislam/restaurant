# from flaskapp.models import Employee, Customer, Menu

# def seed(db):
#     employees = [
#         Employee(id=1, email="eugenef@gmail.com", username="Flynn Rider", password="letdownyourhair", position="delivery"),
#         Employee(id=2, email="levia@gmail.com", username="Levi Ackerman", password="fidgetspinner", position="chef"),
#         Employee(id=3, email="wisegirl@gmail.com", username="Annabeth Chase", password="ih8spiders", position="delivery"),
#         Employee(id=4, email="odasaku@gmail.com", username="Osamu Dazai", password="2xsuicide", position="chef"),
#         Employee(id=5, email="rietveld6@gmail.com", username="Kaz Brekker", password="noMourners", position="delivery"),
#     ]

#     customers = [
#         Customer(id=6, email="twainM@gmail.com", username="Mark Twain", password="TomSawyer", status="registered"),
#         Customer(id=7, email="dickensC@yahoo.com", username="Charles Dickens", password="2Cities", status="vip"),
#         Customer(id=8, email="christieA@gmail.com", username="Agatha Christie", password="OrientXpress", status="registered"),
#         Customer(id=9, email="fitzF@yahoo.com", username="Francis Fitzgerald", password="Gatsby", status="vip"),
#         Customer(id=10, email="steinbeckJ@yahoo.com", username="John Steinbeck", password="GrapesOfWrath", status="registered"),
#     ]

#     menus = [
#         Menu(id=1, name="Waffles", price=8.5, description="Dough-based, caramelized waffle topped with vanilla bean ice-cream", rating=4.3),
#         Menu(id=2, name="Veggie Omelette", price=6, description="Mushrooms, Onions, Peppers", rating=4),
#         Menu(id=3, name="Oatmeal", price=7.25, description="Cinnamon, Honey, Blueberries", rating=3.7),
#         Menu(id=4, name="Chocolate-Chip Pancakes", price=9, description="Maple Syrup, Strawberries", rating=5),
#         Menu(id=5, name="Avocado Toast", price=9.5, description="Sourbread Dough, Tomato, Microgreens", rating=4.6),
#     ]

#     db.session.add_all(employees)
#     db.session.add_all(customers)
#     db.session.add_all(menus)
#     db.session.commit()
