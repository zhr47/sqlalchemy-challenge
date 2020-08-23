# import Flask
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# database_path = "hawaii.sqlite"

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflecting the db
Base = automap_base()
# reflecting the table
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)

# create an app
app = Flask(__name__)

# index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate App Flask API!<br>"
        f"Avaialable routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/start<br>"
        f"/api/v1.0/temp/start/end"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()      
    stations = list(np.ravel(results))       
    return jsonify(stations)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).filter(Measurement.station=='USC00519281').all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)

# date route:
@app.route("/api/v1.0/temp/<start>")
def start(start):
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


# start-end date route:
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start,end):
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)