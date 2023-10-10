from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BusData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(50))
    departure_time = db.Column(db.String(50))
    arrival_time = db.Column(db.String(50))

    def __init__(self, route_number, departure_time, arrival_time):
        self.route_number = route_number
        self.departure_time = departure_time
        self.arrival_time = arrival_time

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
