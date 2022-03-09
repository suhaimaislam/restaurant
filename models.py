
   
from app import db


class Employees(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    position = db.Column(db.String(30), nullable=False)
    # position = db.relationship("Post", back_populates='user')
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position
            # "position": [item.serialize() for item in self.posts]
        }


class Customers(db.Model):
    __tablename__ = "customers"
      
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

      
class Visitors(db.Model):
    __tablename__ = "visitors"
   
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(30), nullable=False)

   def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
