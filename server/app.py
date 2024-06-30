#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/", methods=["GET"])
def index():
    return "<h1>Mark Maina</h1>"

@app.route("/restaurants", methods=["GET"])
def restaurants():
    restaurants = Restaurant.query.all()

    restaurantsjson = []
    for i in restaurants:
        restaurant = i.to_dict(rules= ("-restaurant_pizzas",))
        restaurantsjson.append(restaurant)

    return make_response(restaurantsjson, 200 )


@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def restaurantbyid(id):
    restbyid = Restaurant.query.filter(Restaurant.id == id).first()
    if restbyid:
        if request.method == "GET":
            return make_response(restbyid.to_dict(),200)
        elif request.method == "DELETE":
            db.session.delete(restbyid)
            db.session.commit()
            return make_response({}, 204)
    else :
        return make_response({"error": "Restaurant not found"}, 404)
    
@app.route("/pizzas", methods = ["GET"])    
def pizzas ():
    pizzas = Pizza.query.all()
    
    pizzajson = []
    for i in pizzas:
        pizza = i.to_dict(rules = ("-restaurant_pizzas" ,))
        pizzajson.append(pizza)

    return make_response(pizzajson, 200)    


@app.route("/restaurant_pizzas", methods = ["POST"])
def postrestaurant ():
    if request.method == "POST":
        try :
            restaurant_pizza = RestaurantPizza(
                price = request.get_json()["price"],
                restaurant_id = request.get_json()["restaurant_id"],
                pizza_id = request.get_json()["pizza_id"]
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return make_response(restaurant_pizza.to_dict(), 201)
        except ValueError :
            return make_response({"errors": ["validation errors"]}, 400)



if __name__ == "__main__":
    app.run(port=5555, debug=True)
