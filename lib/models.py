from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = {'-pizzas.restaurants'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    pizzas = db.relationship('Pizza', secondary='restaurant_pizza',back_populates='restaurants')

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'


    serialize_rules = {'-restaurants.pizzas'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    restaurants= db.relationship('Restaurant', secondary='restaurant_pizza',back_populates='pizzas')

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizza'

    serialize_rules = {'-pizzas.restaurants'}

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
