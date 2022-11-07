# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#Import dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependencies for Flask
from flask import Flask, jsonify

# Set up the database engine for Flask
engine = create_engine('sqlite:///hawaii.sqlite')

# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variables for each class for future reference
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from pyton to the database
session = Session(engine)

# Define flask app
app = Flask(__name__)

# Define the welcome route
@app.route('/')

# Create the function 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create the precipitation route
@app.route('/api/v1.0/precipitation')

# Create the preciptation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #calculates the date from one year ago from the most recent date in the database
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >=prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create a route for stations
@app.route('/api/v1.0/stations')   

# Create a new function for stations
def stations():
    results = session.query(Station.station).all() # Create a query that will allow to get all the stations in the database. 
    stations = list(np.ravel(results)) #unravel the results into a 1-D array and then convert the array into a list 
    return jsonify(stations=stations) #return the list as a JSON file 

# create a route for temperature observations
@app.route("/api/v1.0/tobs")

# create a function for monthly temperatures
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) # calculate the date one year ago from the last date in the database
    #quary the primary station for all the temperature observatons from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results)) # unravel the results into a 1-D array and convert the array into a list
    return jsonify(temps=temps) # return the statement as a JSON

# Add routes for temperature analysis (min, max, average)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create stats function to hold the temp analysis
def stats(start = None, end = None): # add parameters to stats; set as none for both
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)] #query to select min, avg, max temps from SQLite database

    #Use if-not statement to determine the starting and ending date. 
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    #Calculate the min, avg, max temperatures with start and end dates. Use the sel list (which is the datapoints we need to collect)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)