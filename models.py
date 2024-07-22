from config import *
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)

class Vehicle(db.Model, SerializerMixin):
    __tablename__ = "vehicles"
    id  = db.Column(db.Integer, primary_key =True)
    vin = db.Column(db.String, nullable= False)
    make = db.Column(db.String)
    location = db.Column(db.String)

class Trip(db.Model, SerializerMixin):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    destination = db.Column(db.String)
    date= db.Column(db.String)

class Maintenance(db.Model, SerializerMixin):
    __tablename__ = "maintenance_records"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String)
    maintenance_type = (db.String)



    