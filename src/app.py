from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from database_models import db, BusData, UserData
from flask import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_data.db'
db.init_app(app)

class Users(db.Model):
    id = db.Column("User_ID", db.Integer, primary_key=True)
    name = db.Column(db.String(20))

@app.route('/analytics')
def analytics():
    total_buses = BusData.query.count()
    total_users = UserData.query.count()
    
    analytics_data = {
        'total_buses': total_buses,
        'total_users': total_users
    }
    
    return jsonify(analytics_data)


@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/add_bus')
def add_bus():
    new_bus = BusData(route_number='123', departure_time='12:30', arrival_time='13:30')
    db.session.add(new_bus)
    db.session.commit()
    return 'Bus added'

@app.route('/show_buses')
def show_buses():
    buses = BusData.query.all()
    all_buses = []
    for bus in buses:
        bus_data = {
            'route_number': bus.route_number,
            'departure_time': bus.departure_time,
            'arrival_time': bus.arrival_time
        }
        all_buses.append(bus_data)
    response = app.response_class(
        response=json.dumps(all_buses, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/fetch_users_and_store')
def fetch_users_and_store():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        data = response.json()

        for user in data:
            new_user = UserData(id=user["id"], name=user["name"], email=user["email"])
            db.session.add(new_user)
        
        db.session.commit()
        
        return jsonify(status='User data fetched and stored')

    except requests.RequestException as e:
        return jsonify(status=f"API request failed: {e}")

    except Exception as e:
        db.session.rollback()
        return jsonify(status=f"An error occurred: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
