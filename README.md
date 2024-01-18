# sqlalchemy-challenge

## Background
The main aim of this project was to analyze climate trends in Hawaii using SQLAlchemy ORM and present the queried results in a Flask API.

## Methods
The climate analysis was conducted using data stored as a SQLite file. There were two different tables, measurement and station, within this relational database. The measurement dataset contained precipitation and temperatures observed each day, while the latter listed stations in Hawaii. The SQLAlchemy functions were used to connect to the SQLite database and reflect our tables into classes.
 
The last 12 months of precipitation data up to the latest date were plotted in a bar graph. The summary statistics for the precipitation data was also computed.

Lastly, we developed a Flask API consisted of five routes based on the climate analysis. The queried results were converted into a dictionary, which then was returned as a JSON list.

The analysis and Flask application were programmed in Jupyter Notebook and Python--there are two files, climate_starter.ipynb and app.py, respectively.

