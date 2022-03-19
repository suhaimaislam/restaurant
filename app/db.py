from app import db
from seed import seed

from models import *

if __name__ == "__main__":
    print("Dropping database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    print("Seeding database tables...")
    seed(db)
    print("Committing...")
    db.session.commit()
    print("Completed!")
