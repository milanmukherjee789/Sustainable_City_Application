import requests
import json
import csv
import geojson
import random

#To get the gecoding from api
def getLocation(loc_name):
    # Mapbox access token
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{loc_name}.json'
    params = {'access_token': ACCESS_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()
    loc = data['features'][0]['center']
    loc = ', '.join(str(item) for item in loc)
    return loc

#To get the direction from api
def direction(start,end):
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    # Specify the API endpoint and parameters
    url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{start};{end}?geometries=geojson&'
    params = {'access_token': ACCESS_TOKEN}
    # Make the API request
    response = requests.get(url, params=params)
    # Get the JSON response
    data = response.json()
    return data

def read():
    cabs = []
    
    feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }
    places1 = ["Dublin Airport","Trinity College Dublin","University College Dublin","Dublin Business School",'Leinster House','Dublin Castle','National Museum of Ireland','Kilmainham Gaol Museum','The National Gallery of Ireland','Dublin Zoo','Glasnevin Cemetery Museum']
    places2 = ["O'Connell Street", "Temple Bar", "St. Stephen's Green",'Grafton Street','Merrion Square','Phoenix Park','St. Patrick Cathedral','Guinness Storehouse','The Spire','THE GPO','Christ Church Cathedral','Grafton Street','James Joyce Centre','Howth','Merrion Square']
    for i in range(20):
        # print(i)
        start = getLocation(random.choice(places1)+",Dublin")
        end = getLocation(random.choice(places2)+",Dublin")
        data = direction(start,end)
        geo = createGeo(data)
        feature_collection['features'] += geo['features']
    for i in range(20):
        feature_collection['features'][i]['properties']['taxi'] = "taxi "+str(i+1)
        # print(feature_collection['features'][0]['type'])
    return feature_collection

def createGeo(data):
    # extract the coordinates from the data
    coordinates = data['routes'][0]['geometry']['coordinates']
    # create a GeoJSON feature collection
    feature_collection = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': coordinates
            },
            'properties': {
                'distance': data['routes'][0]['distance'],
                'duration': data['routes'][0]['duration'],
                'waypoints': [waypoint['name'] for waypoint in data['waypoints']]
            }
        }]
    }
    return feature_collection

def getCab():
    return read()
    # print(l)

