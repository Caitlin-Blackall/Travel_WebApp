from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime

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
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Integer, unique=False)
    accomodation = db.Column(db.String(300), index=True, unique=False)
    travel = db.Column(db.String(300), index=True, unique=False)
    day_overview = db.Column(db.String(300), index=True, unique=False)
    total_cost = db.Column(db.Integer, unique=False)

class TripPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Integer, unique=False)
    non_negotiables = db.Column(db.String(300), index=True, unique=False)
    accomodation = db.Column(db.String(300), index=True, unique=False)
    accomodation_cost = db.Column(db.Integer, unique=False)
    travel = db.Column(db.String(300), index=True, unique=False)
    travel_cost = db.Column(db.Integer, unique=False)
    day_overview = db.Column(db.String(300), index=True, unique=False)
    activity_cost = db.Column(db.Integer, unique=False)
    total_cost = db.Column(db.Integer, unique=False)

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
        place_id = int(request.form['place_id'])

        new_place = Been(city=city, country=country, recommendation=recommendation, review='')

        try:
            place_todelete = Recommendations.query.get_or_404(place_id)
        except:
            place_todelete = Trip.query.get_or_404(place_id)

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
def place(place_id):
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
    trips = TripPlan.query.all()
    return render_template('plan.html', trips=trips)

@app.route('/plan_trip', methods=["GET", "POST"])
def plan_trip():
    if request.method == 'POST':
        cities = ''
        countries = ''
        all_places = ''

        city1 = request.form['city1'].title()
        if city1 != '':
            cities += city1

        country1 = request.form['country1'].title()
        if country1 != '':
            countries += country1

        city2 = request.form['city2'].title()
        if city2 != '':
            cities += ', ' + city2

        country2 = request.form['country2'].title()
        if country2 != '':
            countries += ', ' + country2

        city3 = request.form['city3'].title()
        if city3 != '':
            cities += ', ' + city3

        country3 = request.form['country3'].title()
        if country3 != '':
            countries += ', ' + country3

        old_start_date = request.form['start_date']
        old_start_date = list(old_start_date.split("-"))
        start_year = int(old_start_date[0])
        start_month = int(old_start_date[1])
        start_day = int(old_start_date[2])
        start_date = datetime.date(start_year, start_month, start_day)

        old_end_date = request.form['end_date']
        old_end_date = list(old_end_date.split("-"))
        end_year = int(old_end_date[0])
        end_month = int(old_end_date[1])
        end_day = int(old_end_date[2])
        end_date = datetime.date(end_year, end_month, end_day)

        budget = int(request.form['budget'])
        non_negotiables = request.form['non_negotiables'].capitalize()

        new_tripplan = TripPlan(city=cities, country=countries, start_date=start_date, end_date=end_date, budget=budget,
                                non_negotiables=non_negotiables, accomodation='', accomodation_cost=0, travel='',
                                travel_cost=0, day_overview='', activity_cost=0, total_cost=0)

        db.session.add(new_tripplan)
        db.session.commit()

        return redirect(url_for('trip_planner', trip_id=new_tripplan.id))
    return render_template('plan_trip.html')

@app.route('/<int:trip_id>/trip_planner', methods=["GET", "POST"])
def trip_planner(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)
    first_record = TripPlan.query.get(trip_id)
    # get list of countries
    all_countries = first_record.country
    countries = list(all_countries.split(","))
    # get a list of cities
    all_cities = first_record.city
    cities = list(all_cities.split(","))
    # get a list of accomodation
    all_accomodation = first_record.accomodation
    accomodation = list(all_accomodation.split(','))
    # get a list of travel
    all_travel = first_record.travel
    travel = list(all_travel.split())
    # get a list of activities
    all_activities = first_record.day_overview
    activities = list(all_activities.split(','))
    # get a list of non-negotiables
    all_non_negs = first_record.non_negotiables
    non_negotiables = list(all_non_negs.split(','))
    return render_template('trip_planner.html', trip=trip, countries=countries, cities=cities,
                           accomodation=accomodation, travel=travel, activities=activities,
                           non_negotiables=non_negotiables, trip_id=trip.id)

@app.route('/<int:trip_id>/edit_trip', methods=["GET", "POST"])
def edit_trip(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)

    if request.method == 'POST':

        country = request.form['country'].title()
        city = request.form['city'].title()
        old_start_date = request.form['start_date']
        old_end_date = request.form['end_date']
        budget = request.form['budget']
        non_negotiables = request.form['non_negotiables'].capitalize()
        accomodation = request.form['accomodation'].title()
        old_accomodation_cost = request.form['accomodation_cost']
        travel = request.form['travel'].capitalize()
        old_travel_cost = request.form['travel_cost']
        day_overview = request.form['day_overview'].capitalize()
        old_activity_cost = request.form['activity_cost']

        trip.country = country.title()
        trip.city = city.title()

        old_start_date = list(old_start_date.split("-"))
        start_year = int(old_start_date[0])
        start_month = int(old_start_date[1])
        start_day = int(old_start_date[2])
        start_date = datetime.date(start_year, start_month, start_day)
        trip.start_date = start_date

        old_end_date = list(old_end_date.split("-"))
        end_year = int(old_end_date[0])
        end_month = int(old_end_date[1])
        end_day = int(old_end_date[2])
        end_date = datetime.date(end_year, end_month, end_day)
        trip.end_date = end_date

        trip.budget = int(budget)

        trip.non_negotiables = non_negotiables

        trip.accomodation = accomodation

        if old_accomodation_cost != '':
            old_accomodation_cost = list(old_accomodation_cost.split())
            accomodation_cost = 0
            for cost in old_accomodation_cost:
                cost = int(cost)
                accomodation_cost += cost
            trip.accomodation_cost = accomodation_cost
        else:
            accomodation_cost = 0
            trip.accomodation_cost = accomodation_cost

        trip.travel = travel

        if old_travel_cost != '':
            old_travel_cost = list(old_travel_cost.split())
            travel_cost = 0
            for cost in old_travel_cost:
                cost = int(cost)
                travel_cost += cost
            trip.travel_cost = travel_cost
        else:
            travel_cost = 0
            trip.travel_cost = travel_cost

        trip.day_overview = day_overview

        if old_activity_cost != '':
            old_activity_cost = list(old_activity_cost.split())
            activity_cost = 0
            for cost in old_activity_cost:
                cost = int(cost)
                activity_cost += cost
            trip.activity_cost = activity_cost
        else:
            activity_cost = 0
            trip.activity_cost = activity_cost

        total_cost = accomodation_cost + travel_cost + activity_cost
        trip.total_cost = total_cost

        db.session.add(trip)
        db.session.commit()

        return redirect(url_for('trip_planner', trip_id=trip.id))

    return render_template('edit_trip.html', trip=trip)

@app.route('/finalised_trips', methods=["GET", "POST"])
def finalised_trips():
    trips = Trip.query.all()

    if request.method == 'POST':
        country = request.form['country'].title()
        city = request.form['city'].title()
        old_start_date = request.form['start_date']
        old_end_date = request.form['end_date']
        budget = int(request.form['budget'])
        accomodation = request.form['accomodation'].title()
        travel = request.form['travel'].capitalize()
        day_overview = request.form['day_overview'].capitalize()
        total_cost = int(request.form['total_cost'])
        trip_id = request.form['trip_id']

        old_start_date = list(old_start_date.split("-"))
        start_year = int(old_start_date[0])
        start_month = int(old_start_date[1])
        start_day = int(old_start_date[2])
        start_date = datetime.date(start_year, start_month, start_day)

        old_end_date = list(old_end_date.split("-"))
        end_year = int(old_end_date[0])
        end_month = int(old_end_date[1])
        end_day = int(old_end_date[2])
        end_date = datetime.date(end_year, end_month, end_day)

        new_trip = Trip(city=city, country=country, start_date=start_date, end_date=end_date, budget=budget,
                        accomodation=accomodation, travel=travel, day_overview=day_overview, total_cost=total_cost)
        trip_todelete = TripPlan.query.get_or_404(trip_id)

        db.session.add(new_trip)
        db.session.delete(trip_todelete)
        db.session.commit()
        return redirect(url_for('finalised_trips'))

    return render_template('finalised_trips.html', trips=trips)

#TO START DB
'''
with app.app_context():
    #db.drop_all() #to delete all info in the database
    db.create_all()'''