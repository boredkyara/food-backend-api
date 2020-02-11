from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, Meal

# Connect to Database and create database session
engine = create_engine('sqlite:///restaurant-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/meals')
def showMeals():
    meals = session.query(Meal).all()
    return render_template('meals.html', meals=meals)


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'],
                                   type=request.form['type'],
                                   )
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newBook.html')


@app.route('/restaurants/<int:restaurant_id>/new_meal', methods=['GET', 'POST'])
def newMeal(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newMeal = Meal(name=request.form['name'],
                       restaurant_id=restaurant_id,
                       image_link=request.form['image_link'],
                       price=request.form['price'],
                       description=request.form['description'])
        restaurant.menu = newMeal
        session.add(newMeal)
        session.commit()
        return redirect(url_for('showMeals'))
    else:
        return render_template('newMeal.html')


"""
api functions
"""
from flask import jsonify


def get_restaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


def get_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(restaurants=restaurant.serialize)


def get_meals():
    meals = session.query(Meal).all()
    return jsonify(meals=[m.serialize for m in meals])


def makeANewRestaurant(name, type):
    addedRestaurant = Restaurant(name=name, type=type)
    session.add(addedRestaurant)
    session.commit()
    return jsonify(restaurant=addedRestaurant.serialize)


def makeANewMeal(restaurant_id, image_link, price, name, description):
    addedMeal = Meal(restaurant_id=restaurant_id, image_link=image_link, price=price, name=name, description=description)
    session.add(addedMeal)
    session.commit()
    return jsonify(meal=addedMeal.serialize)


@app.route('/')
@app.route('/restaurantsApi', methods=['GET', 'POST'])
def restaurantsFunction():
    if request.method == 'GET':
        return get_restaurants()
    elif request.method == 'POST':
        name = request.args.get('name', '')
        type = request.args.get('type', '')
        return makeANewRestaurant(name, type)


@app.route('/mealsApi', methods=['GET', 'POST'])
def mealsFunction():
    if request.method == 'GET':
        return get_meals()


@app.route('/mealsApi/<int:id>', methods=['POST'])
def mealsFunctionId(id):
    if request.method == 'POST':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        price = request.args.get('price', '')
        image_link = request.args.get('image_link', '')
        restaurant_id = id
        return makeANewMeal(restaurant_id, image_link, price, name, description)


@app.route('/restaurantsApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurantFunctionId(id):
    if request.method == 'GET':
        return get_restaurant(id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4996)