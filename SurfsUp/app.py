# Import the dependencies.
# I'm going to import all the dependencies from the jupyter notebook
import numpy as np
import pandas as pd
import datetime as dt
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# This is going to be used for the app
# jsonify will take any python dictionary and transfrom it into
# a properly formatted JSON // 

from flask import Flask,jsonify

#################################################
# Database Setup
# this is where we put sqlite and we can use the info from jupyter notebook to populate
#################################################
# Link to database location
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
#Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
# Standard naming
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# using into to flask and api as reference
# Route to Home page
@app.route("/")
def home():
    print("This is a Home page request that list the page routes")
    # Create a f string to display all the routes and use a bit of css code
    return(
        f"Welcome to the Home page<br/>"
        f"List of Available Routes are Below:<br/>"
        f"Precipitation Aug 23, 2016 to Aug 23, 2017 Route: /api/v1.0/precipitation<br/>"
        f"Station Route: /api/v1.0/stations<br/>"
        f"Temperatures Between Aug 23, 2016 to Aug 23, 2017 Route: /api/v1.0/tobs<br/>"
        f"Temperature Start Route: /api/v1.0/<start><br/>"
        f"Temperature End Route: /api/v1.0/<start>/<end><br/>"
    )

# Route to Precipitation Aug 23, 2016 to Aug 23, 2017 page
# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

#@app.route("/api/v1.0/precipitation")
#def precipitation():
 #   session = Session(engine)
  #  select = 

# Route to Station page
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
# This is pulling info from the sqlite database
def stations():
    session = Session(engine)
    select = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    queryresult = session.query(*select).all()
    session.close()

# Create a list and dictionary and jsonify the dictionary so it looks nice on the web page
    stations = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

# Route to Temperatures Between Aug 23, 2016 to Aug 23, 2017 page



# Route to Temperature Start page
# Route to Temperature End page

#dynamic route. if ony start date given, end date default is none.
@app.route('/api/v1.0/<start>', defaults = {'end':None})
@app.route("/api/v1.0/<start>/<end>")
def temps_for_date_range(start, end):
#Open session and do if statement where if end date is given, temp data calculated filters incorporate end dates to get range. if no end date given, temp calculations only use start date.
    session = Session(engine)
    if end != None:
        min_temp = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
        max_temp = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
        avg_temp = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
        
    else:
        min_temp = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all()
        max_temp = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all()
        avg_temp = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()
    
    
    #capture variables
    print("min_temp output:", min_temp)
    print("max_temp output:", max_temp)
    print("avg_temp output:", avg_temp)

#     #go in to the variable and extract just the temps needed. current format is single tuple with single value and comma
    min_temp = min_temp[0][0]
    max_temp = max_temp[0][0]
    avg_temp = avg_temp[0][0]

    results = {
        "Min temp": min_temp,
        "Max temp": max_temp,
        "Average temp": avg_temp
     }


if __name__ == '__main__':
    app.run(debug=True)


