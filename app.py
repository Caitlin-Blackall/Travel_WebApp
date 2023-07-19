from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_webapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    recommendation = db.Column(db.String(150), index=True, unique=False)

class Been(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    recommendation = db.Column(db.String(300), index=True, unique=False)
    review = db.Column(db.String(150), index=True, unique=False)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    travel = db.Column(db.String(300), index=True, unique=False)
    budget = db.Column(db.Integer, unique=False)
    total_cost = db.Column(db.Integer, unique=False)
    day_overview = db.Column(db.String(300), index=True, unique=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/places_togo', methods=["GET", "POST"])
def places_togo():
    recommendations = Recommendations.query.all()
    return render_template('places_togo.html', recommendations=recommendations)

@app.route('/add_recommendation', methods=["GET", "POST"])
def add_recommendation():
    if request.method == 'POST':
        city = request.form['city'].title()
        country = request.form['country'].title()
        recommendation = request.form['recommendation'].capitalize()
        new_recommendation = Recommendations(city=city, country=country, recommendation=recommendation)
        db.session.add(new_recommendation)
        db.session.commit()
        return redirect(url_for('places_togo'))
    return render_template('add_recommendation.html')

@app.route('/places_been', methods=["GET", "POST"])
def places_been():
    places_been = Been.query.all()

    if request.method == 'POST':
        city = request.form['city'].title()
        country = request.form['country'].title()
        recommendation = request.form['recommendation'].capitalize()
        place_id = request.form['place_id']

        new_place = Been(city=city, country=country, recommendation=recommendation, review='')
        place_todelete = Recommendations.query.get_or_404(place_id)

        db.session.add(new_place)
        db.session.delete(place_todelete)
        db.session.commit()

        return redirect(url_for('places_been'))

    return render_template('places_been.html', places_been=places_been)

@app.route('/countries', methods=["GET", "POST"])
def countries():
    all_countries = []
    all_info = Been.query.all()
    for info in all_info:
        all_countries.append(info.country)
    unique_countries = []
    for country in all_countries:
        if country not in unique_countries:
            unique_countries.append(country)
    return render_template('countries.html', unique_countries=unique_countries)

@app.route('/cities', methods=["GET", "POST"])
def cities():
    all_cities = []
    all_info = Been.query.all()
    for info in all_info:
        all_cities.append(info.city)
    unique_cities = []
    for city in all_cities:
        if city not in unique_cities:
            unique_cities.append(city)
    return render_template('cities.html', unique_cities=unique_cities)

@app.route('/<int:place_id>/')
def recipe(place_id):
    place = Been.query.get_or_404(place_id)
    return render_template('place.html', place=place)

@app.route('/<int:place_id>/review/', methods=('GET', 'POST'))
def review(place_id):
    place = Been.query.get_or_404(place_id)

    if request.method == 'POST':
        city = request.form['city'].title()
        country = request.form['country'].title()
        recommendation = request.form['recommendation'].capitalize()
        review = request.form['review'].capitalize()

        place.city = city
        place.country = country
        place.recommendation = recommendation
        place.review = review

        db.session.add(place)
        db.session.commit()

        return redirect(url_for('places_been'))

    return render_template('review.html', place=place)

@app.route('/plan', methods=["GET", "POST"])
def plan():
    return render_template('plan.html')


#TO START DB
'''
with app.app_context():
    #db.drop_all() #to delete all info in the database
    db.create_all()'''