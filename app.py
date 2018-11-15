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
    return (f"Welcome To Hawaii Vacation Planner!<br>"
            f"Page Available Routes:<br>"
            f"Precipitaion: /api/v1.0/precipitation<br>"
            f"Weather Stations: /api/v1.0/stations<br>"
            f"Temperature: /api/v1.0/tobs"
            )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a date and precipitation"""
    # Query date and prcp
    results = session.query( Measurement.date, Measurement.prcp).\
    order_by(Measurement.date).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))
    
    prcp = []
    prcp_dict = {}
    for row in results:
        if row[0] not in prcp_dict:
            prcp_dict[row[0]] = {}
            prcp_dict[row[0]] = row[1]
        prcp.append(prcp_dict)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations from the dataset"""
    # Query date and prcp
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).all()
    
    # Convert list of tuples into normal list
    station_data = list(np.ravel(stations))
    station_dict = {}
    for i in range(len(station_data)):
        station_dict['Station'] = station_data[i]

    return jsonify(station_dict)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/api/v1.0/tobs")
def temp():
    """Return the dates and temperature observations from a year from the last data point"""
    # Query date and prcp
    obs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    # Convert list of tuples into normal list
    obs_data = list(np.ravel(obs))

    obs_list = []
    obs_dict = {}
    for row in obs:
        if row[0] not in obs_dict:
            obs_dict[row[0]] = {}
            obs_dict[row[0]] = row[1]
        obs_list.append(obs_dict)

    return jsonify(obs_list)

if __name__ == '__main__':
    app.run(debug=True)

