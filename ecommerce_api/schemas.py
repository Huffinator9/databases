# src ./schemas.py

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import User, Order, Product

# User Schema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        sqla_session = None

    #extra validation
    email = fields.Email(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    address = fields.String(validate=validate.Length(max=200))

# Order Schema

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        inlude_relationships = True
        include_fk = True # ensures "user_id" shows up
        sqla_session = None

    # show "order_date" in ISO format
    order_date = fields.DateTime(dump_only=True)

# Product Schema

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_relationships = True
        sqla_session = None

    product_name = fields.String(required=True, validate=validate.Length(min=1, max=150))
    price = fields.Float(required=True, validate=validate.Range(min=0))
