from flask import request, jsonify, Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
# from flask_sqlalchemy import __init__ 
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False



migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
api = Api(app)
from models import Restaurant, Pizza, RestaurantPizza


class Restaurants(Resource):
    def get(self):
        # re
        restaurant_dict = [rest.to_dict() for rest in Restaurant.query.all()]
        return make_response(jsonify(restaurant_dict), 200)
    
api.add_resource(Restaurants,'/restaurants')

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    print(restaurant)
    if restaurant:
        restaurant_data = restaurant.to_dict()
        #     'id': restaurant.id,
        #     'name': restaurant.name,
        #     'address': restaurant.address,
        #     'pizzas': [
        #         {
        #             'id': pizza.id,
        #             'name': pizza.name,
        #             'ingredients': pizza.ingredients
        #         }
        #         for pizza in restaurant.pizzas
        #     ]
        # }
        return jsonify(restaurant_data)
    return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Restaurant not found'}), 404


# class Pizzas(Resource):
#     def get(self):
#         pizza_dict = [pizza.to_dict() for pizza in Pizza.query.all()]
#         return make_response(jsonify(pizza_dict), 200)
    
# api.add_resource(Pizza, '/pizzas')


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    
    

    restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(restaurant_pizza)
    db.session.commit()

    pizza = Pizza.query.get(pizza_id)
    pizza_data = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }
    return jsonify(pizza_data), 201

if __name__ == '__main__':
    app.run(debug=True)
