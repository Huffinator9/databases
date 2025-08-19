# src ./routes.py

from flask import Blueprint, request, jsonify
from models import db, User, Order, Product
from schemas import UserSchema, OrderSchema, ProductSchema

api_blueprint = Blueprint("api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# User CRUD
@api_blueprint.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@api_blueprint.route("/users/<int:id>", methods=["GET"])
def get_users(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

@api_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@api_blueprint.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user)

@api_blueprint.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# Product CRUD
@api_blueprint.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@api_blueprint.route("/products/<int:id>", methods=["GET"])
def get_products(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@api_blueprint.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = product_schema.load(data)
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@api_blueprint.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return product_schema.jsonify(product)

@api_blueprint.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})

# Order CRUD
@api_blueprint.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    order = order_schema.load(data)
    db.session.add(order)
    db.session.commit()
    return order_schema.jsonify(order), 201

@api_blueprint.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
                                                                                    
    if product in order.products:
        return jsonify({"message": "Product already in order"}), 400

    order.products.append(product)
    db.session.commit()
    return order_schema.jsonify(order)

@api_blueprint.route("/orders/<int:order_id>/remove_product/<int:product_id>", methods=["DELETE"])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
                                                                                    
    if product not in order.products:
        return jsonify({"message": "Product not in order"}), 400

    order.products.remove(product)
    db.session.commit()
    return order_schema.jsonify(order)

@api_blueprint.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_for_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return orders_schema.jsonify(orders)

@api_blueprint.route("/orders/<int:order_id>/products", methods=["GET"])
def get_products_for_order(order_id):
    order = Order.query.get_or_404(order_id)
    return products_schema.jsonify(order.products)
