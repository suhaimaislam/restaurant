from flaskapp import app, db
from flaskapp.models import *

if __name__ == '__main__':
    print("Dropping database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    print("Completed!")
    app.run(debug=True)
