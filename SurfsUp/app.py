# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, or_, not_
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement #station,date,prcp,tobs
Station = Base.classes.station #station,name,latitude,longitude,elevation

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################


# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "<div><h1>Surfs Up Dude</h1><h3>Welcome to the only app you need to plan your trip</h3><h3>Here are the available routes</h3><p>/api/v1.0/precipitation</p><p>/api/v1.0/stations</p><p>/api/v1.0/tobs</p><p>/api/v1.0/[start]</p><p>/api/v1.0/[end]</p></div>"


# 4. Define what to do when a user hits the various routes
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = list(np.ravel(results))
    return jsonify(precip=precip)
    session.close()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    data = session.query(Station.station, Station.name).all()
    stations = list(np.ravel(data))
    return jsonify(stations=stations)
    session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(Measurement.tobs, Measurement.date).filter(and_(Measurement.station == 'USC00519281'), (Measurement.date >= prev_year)).all()

    station_data = list(np.ravel(data))
    return jsonify(station_data=station_data)
    session.close()

@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'start' page...")
    return "start Page"

@app.route("/api/v1.0/<end>")
def end():
    print("Server received request for 'End' page...")
    return "End Page"


if __name__ == "__main__":
    app.run(debug=True)


