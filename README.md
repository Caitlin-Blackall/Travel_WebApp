# Travel WebApp

*Completed July 2023*

## Project Overview
I have recently completed a Flask WebApp course and wanted to
put some of the skills I learnt into practice. I have always 
loved travelling and have often wanted an easy way to track 
recommendations, places I have been and to plan trips. This 
seemed like the perfect opportunity to create a Flask WebApp for
this.

## Local Dev Set-Up
### Pre-Requisites:
+ [pip](https://pypi.org/project/pip/)
+ [venv](https://docs.python.org/3/library/venv.html)
+ [Git](https://git-scm.com/)

### Installations:
+ ```pip install flask```
+ ```pip install flask_wtf```
+ ```pip install flask_sqlalchemy```

### Database Set-Up:
The database is managed with SQL via SQLAlchemy. When the project is 
first initialised, the database needs to be created using the following 
command:
```python
with app.app_context():
    db.create_all()
```

To delete all models and data within the database, use the following command:
```python
with app.app_context():
    db.drop_all()
```

### Running the App
This project is run locally only. As such, in order to access the 
app, a local copy must be made first.

1. Enter the directory where the clone will be made.


2. ```git clone [enter SSH key here]```

Once a clone has been made, the app can be activated.

1. ```source bin/activate```


2. ```flask run```


The app will then be accessible on the local development server.

To close the app when finished, use ```^C``` followed by ```deactivate```.

## Development Process
I knew that I wanted 4 different sections in this project - 
a home page, recommendations on where to go, a list 
of where I had been and a section dedicated to trip planning.

Each section needed a navigation bar as well as content 
set out in an easy-to-read way. I used HTML to render templates 
as well as CSS as a separate styling sheet to keep my code 
organised. I created a base.html template which was used 
across all pages of my WebApp as well as an index.html template 
for the home page which included a background image.

I created models using SQLAlchemy to store the data that would 
be used across the WebApp. I needed 4 different models (1 for 
recommendations, 1 for places I had been and 2 for the trip 
planning section).

I then created app routes and functions for each of my sections 
and ensured that I could access data from each model as needed. 
I also used forms to create ways for the user to interact with 
the WebApp and enter new recommendations, plan trips and edit 
trips. I also utilised the button functionality of the forms to 
enable data to be submitted and moved across different sections 
of the WebApp (ie. moving places from 'Places to Go' to 'Places 
I've Been'). Each of the app routes / functions were then 
rendered to a HTML template with the appropriate variables.

Within certain functions, I had to ensure that the data entered 
in the form was able to be saved to the correct model. I did this 
using db.session.add(variable) and db.session.commit() as well 
as removing data from models when it was no longer required (ie. 
removing data from 'Places to Go' when it was submitted to 
'Places I've Been'.)

## Learning
### Challenges
By far the biggest challenge of this project was dealing with 
the data. I needed to make sure that my data was being 
processed appropriately within the correct function and stored 
to the correct model / database. Learning how to make a form 
with 'hidden' properties was definitely useful to ensure that 
I could link pages together while also creating appropriate 
POST request in order to ensure that the data also moves to 
the right model / page of the WebApp.

### New Skills

**1. Flask**

The major new skill I learnt during this project was Flask. It 
was initially challenging at times, especially learning how to 
connect routes to functions and templates. Learning to render 
templates and design these within HTML was also challenging at 
times, especially when needing to redirect to urls.

However, the further into the development of the app, the easier 
this became. I learnt a lot about using different styling within 
a separate styling sheet and this is something that I could 
definitely continue to work on to ensure less overlap of 
styling for different elements.

**2. SQLAlchemy & FlaskForms/Jinga2 Templates**

Using SQLAlchemy and incorporating this into code was challenging 
at times, especially when needing to move data across multiple 
different webpages. By the end of the project, I had become 
more confident with GET and POST methods which definitely helped 
me to develop the functionality of the app further. I was able 
to access models within SQLAlchemy and change data in these using 
forms and templates which was great. As discussed below, it would 
be ideal to be able to use relational databases to prevent 
information being copied multiple times to enable functionality 
of the website.


## Future Work
I would ideally like to be able to add pictures to the site 
as new trips were completed. I would also like to work on the 
display of the website and incorporate more image elements into 
each page to enhance the web display.

It would also be nice to further explore relational 
databases and utilise some of this functionality. At the moment, 
there is a database for each webpage. It would be best to try 
and utilise relational databases to stop the crossover of data 
entry. This would also help keep the code a bit neater.

When trips are planned across multiple cities and countries, 
there is currently no functionality to split countries and 
therefore two countries can be displayed on the same line in 
'Places Been'. This is something that I would like to address 
in future to make the webapp more functional. Exploring ways to 
display cities grouped by countries in 'Cities Visited' would 
also be great.

## Conclusion
Overall, this was a lot more challenging than my last project 
but it was also super rewarding to create a more functional 
WebApp. I learnt a lot about using Flask as well as how useful 
templates are! It was great to be able to put some of the 
things I learnt in my course into practise and there is 
definitely more features that I could add to this project 
in future.