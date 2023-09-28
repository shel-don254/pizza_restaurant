from models import db, Restaurant, Pizza, RestaurantPizza
from lib.app import app
from faker import Faker

fake = Faker()

with app.app_context():
    #enterflask application
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    # /loop
    for _ in range(3):
        restaurant = Restaurant(name=fake.company(), address=fake.address())
        restaurants.append(restaurant)
        db.session.add_all(restaurants)
        db.session.commit()

    pizzas = []
    for _ in range(3):
        pizza = Pizza(name=fake.word(), ingredients=fake.sentence(nb_words=6))
        pizzas.append(pizza)
        db.session.add_all(pizzas)
        db.session.commit()

    restaurant_pizzas = []
    for restaurant in restaurants:
        for pizza in pizzas:
            price = fake.random_element(elements=(9.99, 10.99, 11.99, 12.99, 13.99, 14.99))
            restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
            restaurant_pizzas.append(restaurant_pizza)
            
            db.session.add_all(restaurant_pizzas)
            db.session.commit()




