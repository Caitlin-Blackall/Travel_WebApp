from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime

'''initiates the app'''
app = Flask(__name__)

'''handles app configuration and location of the database'''
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_webapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''initiates the database and links it to the app'''
db = SQLAlchemy(app)

class Recommendations(db.Model):
    '''create the model used to store place recommendations'''
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    recommendation = db.Column(db.String(150), index=True, unique=False)

class Been(db.Model):
    '''create the model used to store places that I've been to'''
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), index=True, unique=False)
    country = db.Column(db.String(100), index=True, unique=False)
    recommendation = db.Column(db.String(300), index=True, unique=False)
    review = db.Column(db.String(150), index=True, unique=False)

class Trip(db.Model):
    '''create the model used to store finalised trip itineraries'''
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
    '''create the model used to create and store trip plans'''
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
    '''
    returns the template for the homepage
    '''
    return render_template('index.html')

@app.route('/places_togo', methods=["GET", "POST"])
def places_togo():
    '''
    access the Recommendations model and passes these to the places_togo.html template
    the template is returned on /places_togo URL
    '''
    recommendations = Recommendations.query.all()
    return render_template('places_togo.html', recommendations=recommendations)

@app.route('/add_recommendation', methods=["GET", "POST"])
def add_recommendation():
    '''
    returns template that contains a form where recommendations can be added
    if the form is submitted (ie. the request.method == 'POST'), the data within the form is accessed,
        an instance of the Recommendations model is then created,
        the data from the form is then saved (added and committed) to the database session
        and finally the user is redirected to the url for places_togo
    if the form is not submitted, the template for add_recommendation.html is displayed at the URL /add_recommendation
    '''
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
    '''
    accesses the Been model and displays all the places that I've been according to the places_been template
    if the user has been directed to this page from a different webpage (ie. redirected from 'Places to Go' or
        'Trip Review'), the information from the form submitted in those templates is accessed and saved as a new
        instance of the Been model
        as there are two routes that can be redirected here, it needs to be clear where the data needs to be removed from
        this is addressed in the try/except statements
        the data is then saved to the Been model and deleted from either the Recommendation model or the Trip model
    the user is then redirected to the places_been.html template at /places_been URL
    '''
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
    '''
    accesses the Been model and creates a list of all the countries within this model
    then iterates through this list, adding unique countries only to a new list
    this new list is then displayed on the countries.html template at URL for /countries
    '''
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
    '''
    accesses the Been model and creates a list of all the cities within this model
    then iterates through this list, adding unique cities only to a new list
    this new list is then displayed on the cities.html template at URL for /cities
    '''
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
    '''
    place_id has been passed to this function
    the information for this specific places is accessed via the Been model using the place_id
    this information is then passed to the template
    place details are then displayed using the place.html template
    the URL receives the place_id as an argument as well, ensuring each place will have its own specific URL
    '''
    place = Been.query.get_or_404(place_id)
    return render_template('place.html', place=place)

@app.route('/<int:place_id>/review/', methods=('GET', 'POST'))
def review(place_id):
    '''
    this function also receives place_id as an argument
    the information for this specific place is accessed through the Been model using the place_id
    this page displays a template review.html at the specific place/review URL
    within this template, a user can enter a review for the trip or place that has been visited
    this function then retrieves this information, updates the Been model for this place with the information,
        saves it and commits it to the database
    the user is then redirected to places_been
    '''
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
    '''
    the TripPlan model is accessed and passed to the template
    all results are displayed using the plan.html template at URL for /plan
    '''
    trips = TripPlan.query.all()
    return render_template('plan.html', trips=trips)

@app.route('/plan_trip', methods=["GET", "POST"])
def plan_trip():
    '''
    the user is shown a form using the template plan_trip.html where they can add details to make a trip plan
        within this form, there are 3 different boxes for each country the trip will involve and the cities that will
            be seen in each country
    this form is then accessed with some extra formatting needed to ensure it can be utilised properly
        the cities are made into one string, as are the countries in order to be passed to the TripPlan model
        the date is then formatted from Jinga2 template date to python date
    a new instance of the TripPlan model is then created, added and saved to the database session
        some of the arguments in TripPlan are not included on the form, so these are passed in as blank strings to the new
            instance of the model
    the user is then redirected to trip_planner, where they can view and add further details of the trip
        the id for the new trip is also passed to trip_planner as an argument to ensure this page can be accessed properly
            (trip_planner URL is <trip_id>/trip_planner)
    '''
    if request.method == 'POST':
        cities = ''
        countries = ''

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
    '''
    this function allows users to see an overview of a specific trip plan
    it takes trip_id as an argument to ensure that only one trip is displayed
    trip_id is passed to TripPlan to access the information for that trip
    the information then has to be processed so it can be displayed nicely within the template trip_planner.html
        as the cities, countries, accomodation, travel, activities and non-negotiables are stored as strings within
            the model, these have to be processed to be displayed properly within the template
        each of these elements is accessed, the string is split and created into a list
        this list is then passed to the template to be rendered out
    '''
    trip = TripPlan.query.get_or_404(trip_id)
    first_record = TripPlan.query.get(trip_id)

    all_countries = first_record.country
    countries = list(all_countries.split(","))

    all_cities = first_record.city
    cities = list(all_cities.split(","))

    all_accomodation = first_record.accomodation
    accomodation = list(all_accomodation.split(','))

    all_travel = first_record.travel
    travel = list(all_travel.split())

    all_activities = first_record.day_overview
    activities = list(all_activities.split(','))

    all_non_negs = first_record.non_negotiables
    non_negotiables = list(all_non_negs.split(','))

    return render_template('trip_planner.html', trip=trip, countries=countries, cities=cities,
                           accomodation=accomodation, travel=travel, activities=activities,
                           non_negotiables=non_negotiables, trip_id=trip.id)

@app.route('/<int:trip_id>/edit_trip', methods=["GET", "POST"])
def edit_trip(trip_id):
    '''
    this function also takes trip_id as an argument to ensure that the specific trip can be edited
    the TripPlan model is accessed using the trip_id and the information displayed on the page according to the
        edit_trip.html template
    the template will display the information within a form so that information can be edited if needed
    the information retrieved from the form using the request.method == 'POST' part of the code is then processed
        the dates are processed in the same way as the above function
        for each section involving a cost, an if/else statement is used to enable use of the sum method to calculate the
            cost of each section as well as the overall cost of the trip
    the information taken from the form is then passed back into the TripPlan model and the changes are saved
    the user is then redirected to trip_planner
    '''
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
    '''
    on this page, all finalised trips are displayed using the finalised_trips.html template at the URL for /finalised trips
    the information is accessed using a query of the Trip model and then passed to the template as an argument
    this page can also be accessed by clicking the 'finalise trip' button on the trip_plan webpage
        clicking this button submit certain information via a POST request
        this information is then accessed, processed and saved as a new instance of the Trip model
        the information is then deleted from the model it was previously stored in (TripPlan)
    the user is then returned to the URL for finalised_trips
    '''
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

#TO START DB ONLY
'''
with app.app_context():
    #db.drop_all() #to delete all info in the database
    db.create_all()'''