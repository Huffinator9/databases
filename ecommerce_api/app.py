# src ./app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Order, Product, OrderProduct
from routes import api_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dev:#NWTdevPW1331@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register routes
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create non-existent tables
    app.run(debug=True)
