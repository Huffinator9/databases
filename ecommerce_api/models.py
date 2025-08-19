#src ./models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Table

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 0001 - xxxx relationship to orders
    orders = db.relationship("Order", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

# Order Table

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # xxxx - xxxx relationship w/ products via order_product
    products = db.relationship(
        "Product",
        secondary="order_product",
        back_populates="orders"
        )

    def __repr__(self):
        return f"<Order {self.id}>"

# Product Table
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # xxxx - xxxx relationship w/ orders via order_product
    orders = db.relationship(
        "Order",
        secondary="order_product",
        back_populates="products"
        )

    def __repr__(self):
        return f"<Product {self.product_name}>"

# Association Table
class OrderProduct(db.Model):
    __tablename__ = "order_product"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)

    # composite pk prevents duping in same order
    __table_args__ = (
        db.UniqueConstraint("order_id", "product_id", name="uq_order_product"),
        )
    def __repr__(self):
        return f"<OrderProduct order_id={self.order_id}, product_id={self.product_id}>"
