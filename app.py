import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,request, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (f"Dear Guest, Welcome To Honululu HI Vacation Planner!<br>"
            f"This page will allow you to get prepared for your vacation. Please follow this routes to find information you need:<br>"
            f"You can access Precipitation Data by following this route: /api/v1.0/precipitation<br>"
            f"You can access Weather Stations Data by following this route: /api/v1.0/stations<br>"
            f"You can access Temperature Data by following this route: /api/v1.0/tobs<br>"
            f"You can access Temperature Data starting from date you choose by following this route: /api/v1.0/<start><br>"
            f"You can access Temperature Data for specific period(start/end) on you choice by following this route: /api/v1.0/<start>/<end>"
            )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a date and precipitation"""
    #Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).\
    order_by(Measurement.date).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))
    
    prcp = []
    for i in results:
        prcp_dict = {}
        prcp_dict[i[0]] = i[1]
        prcp.append(prcp_dict)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations from the dataset"""
    # Query date and prcp
    stations = session.query(Station.name).all()
    
    # Convert list of tuples into normal list
    station_data = list(np.ravel(stations))
    
    station_names = []
    for i in range(len(station_data)):
        station_dict = {}
        station_dict['Station'] = station_data[i]
        station_names.append(station_dict)
    return jsonify(station_names)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/api/v1.0/tobs")
def temp():
    """Return the dates and temperature observations from a year from the last data point"""
    # Query date and prcp
    tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
    order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(tobs))

    tobs_list = []
    for tob in tobs:
        tobs_dict = {}
        tobs_dict['Date'] = tob.date
        tobs_dict['Temp(F)'] = tob.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/api/v1.0/<start>")
def start(start):
    return (f"Please enter start date. (example: 2017-07-17)<br>")
    """Return the MIN, AVG, MAX temperature observations from the selected data point"""
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)). group_by(Measurement.date).filter(Measurement.date >= start_date).all()

    start_list = []
    for result in results:
        start_dict = {}
        start_dict[result[0]] = {}
        start_dict[result[0]]['MIN'] = result[1]
        start_dict[result[0]]['AVG'] = result[2]
        start_dict[result[0]]['MAX'] = result[3]
        start_list.append(start_dict)

    return jsonify(start_list)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    return (f"Please enter start and end date. (example: 2017-07-17/2017-07-27)<br>")
    """Return the MIN, AVG, MAX temperature observations between selected dates"""
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    results = session.query(Measurement.date,func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)).\
    group_by(Measurement.date).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    startend_list = []
    for result in results:
        startend_dict = {}
        startend_dict[result[0]] = {}
        startend_dict[result[0]]['MIN'] = result[1]
        startend_dict[result[0]]['AVG'] = result[2]
        startend_dict[result[0]]['MAX'] = result[3]
        startend_list.append(startend_dict)

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)
