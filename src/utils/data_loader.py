import pandas as pd
import os

def load_airports(file_path):
    airport_cols = ['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO',
                    'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST',
                    'Tz', 'Type', 'Source']
    airports = pd.read_csv(file_path, names=airport_cols, index_col=False, header=None)
    return airports

def load_routes(file_path):
    route_cols = ['Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID',
                  'DestAirport', 'DestAirportID', 'Codeshare', 'Stops', 'Equipment']
    routes = pd.read_csv(file_path, names=route_cols, index_col=False, header=None)
    # Filter out invalid routes
    routes = routes[routes['SourceAirport'].notnull() & routes['DestAirport'].notnull()]
    routes = routes[routes['SourceAirport'] != routes['DestAirport']]
    return routes

def load_data(airports_file, routes_file):
    airports = load_airports(airports_file)
    routes = load_routes(routes_file)
    return airports, routes

def preprocess_data(airports, routes):
    return airports, routes