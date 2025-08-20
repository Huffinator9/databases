# src ./routes.py

from flask import Blueprint, request, jsonify
from models import db, User, Product, Order
from schemas import UserSchema, ProductSchema, OrderSchema

api_blueprint = Blueprint("api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# ---------------------------
# USER CRUD
# ---------------------------
@api_blueprint.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@api_blueprint.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@api_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@api_blueprint.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@api_blueprint.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


# ---------------------------
# PRODUCT CRUD
# ---------------------------
@api_blueprint.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@api_blueprint.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product_schema.dump(product))

@api_blueprint.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = product_schema.load(data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 201

@api_blueprint.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify(product_schema.dump(product))

@api_blueprint.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


# ---------------------------
# ORDER CRUD
# ---------------------------
@api_blueprint.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    order = order_schema.load(data)
    db.session.add(order)
    db.session.commit()
    return jsonify(order_schema.dump(order)), 201

@api_blueprint.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)

    if product in order.products:  # ✅ prevents duplicates
        return jsonify({"message": "Product already in order"}), 400

    order.products.append(product)
    db.session.commit()
    return jsonify(order_schema.dump(order))

@api_blueprint.route("/orders/<int:order_id>/remove_product/<int:product_id>", methods=["DELETE"])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)

    if product not in order.products:
        return jsonify({"message": "Product not in order"}), 400

    order.products.remove(product)
    db.session.commit()
    return jsonify(order_schema.dump(order))

@api_blueprint.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_for_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(orders))

@api_blueprint.route("/orders/<int:order_id>/products", methods=["GET"])
def get_products_for_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(products_schema.dump(order.products))
