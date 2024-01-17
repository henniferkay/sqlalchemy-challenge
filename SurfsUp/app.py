# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the tables
Precipitation = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Hawaii!<br/>"
        f"Before you take off, learn about the latest climate trends<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures observed at the most active station for one year: /api/v1.0/tobs<br/>"
        f"Temperatures observed from start date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperatures observed from start to end dates (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data from the last 12 months"""
    # Query the precipitation data 
    results = session.query(Precipitation.station, Precipitation.date, Precipitation.prcp).\
                filter(Precipitation.date >= '2016-08-24').\
                filter(Precipitation.date <= '2017-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list
    prcp_12mo = []
    for station,date,prcp in results:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        prcp_12mo.append(prcp_dict)

    return jsonify(prcp_12mo)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of observed temperatures of the most active station from the last 12 months"""
    # Query all observed temperatures
    results = session.query(Precipitation.station, Precipitation.date, Precipitation.tobs).\
                filter(Precipitation.date >= '2016-08-24').\
                filter(Precipitation.date <= '2017-08-23').\
                filter(Precipitation.station == 'USC00519281').all()

    session.close()

     # Create a dictionary from the row data and append to a list
    all_tobs = []
    for station,date,tobs in results:
            tobs_dict = {}
            tobs_dict["station"] = station
            tobs_dict["date"] = date
            tobs_dict["tobs"] = tobs
            
            all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the minimum, average and maximum temperatures observed for a specified start date"""
    # Query the oberved temperature data
    results = session.query(func.min(Precipitation.tobs),
                            func.max(Precipitation.tobs),
                            func.avg(Precipitation.tobs)).\
                            filter(Precipitation.date >= start).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list
    start_date_tobs = []
    for min,max,avg in results:
            start_date_tobs_dict = {}
            start_date_tobs_dict["min_temp"] = min
            start_date_tobs_dict["max_temp"] = max
            start_date_tobs_dict["avg_temp"] = avg

            start_date_tobs.append(start_date_tobs_dict)

    return jsonify(start_date_tobs)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the minimum, average and maximum temperatures observed from start to end dates"""
    # Query the oberved temperature data
    results = session.query(func.min(Precipitation.tobs),
                            func.max(Precipitation.tobs),
                            func.avg(Precipitation.tobs)).\
                            filter(Precipitation.date >= start).\
                            filter(Precipitation.date <= end).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list
    start_end_date_tobs = []
    for min,max,avg in results:
            start_end_date_tobs_dict = {}
            start_end_date_tobs_dict["min_temp"] = min
            start_end_date_tobs_dict["max_temp"] = max
            start_end_date_tobs_dict["avg_temp"] = avg

            start_end_date_tobs.append(start_end_date_tobs_dict)

    return jsonify(start_end_date_tobs)

if __name__ == '__main__':
    app.run(debug=True)
