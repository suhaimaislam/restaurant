
   
from app import db


class Employees(db.Model):
    __tablename__ = "employees"

    def serialize(self):
        return {}


class Customers(db.Model):
    __tablename__ = "customers"


    def serialize(self):
        return {}

      
class Visitors(db.Model):
    __tablename__ = "visitors"


    def serialize(self):
        return {}
