import requests
import random
import osmnx as ox
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import networkx as nx

def getLocation(loc_name):
    # Convert location name to Latitude and longitude using MapBox API
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{loc_name}.json'
    params = {'access_token': ACCESS_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()
    loc = data['features'][0]['center']
    loc = ', '.join(str(item) for item in loc)
    return loc


def createGeo(coor):
    # To form the geojson that can be viewed of OpenStreeMap
    feature_collection = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': coor
            },
            'properties': {}
        }]
    }
    return feature_collection

def isochrome(longitude, latitude):
    # To form a figure on the map to mark the accident spot using MapBox API
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    center = f'{longitude},{latitude}'
    url = f'https://api.mapbox.com/isochrone/v1/mapbox/driving/{center}?contours_meters=150&'
    params = {'access_token': ACCESS_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()
    #To convet the recieved geojson to a form that can be read by OpenStreetMap
    coor = createGeo(data['features'][0]['geometry']['coordinates'])
    return coor

def reroute(start, end, loc):
    # To get the latitude and longitude for start, end and centre location received from twitter
    distance_to_avoid = 0.005
    float(getLocation(start).split(',')[0])
    origin = list(map(float, getLocation(start).split(',')))
    destination = list(map(float, getLocation(end).split(',')))
    center = list(map(float, getLocation(loc).split(','))) 
    #To form a box around the accident spot  of around 1000 meters in hieght and 1000 meters in width
    point_bottom_left = (center[0]-distance_to_avoid,center[1]-distance_to_avoid)
    point_bottom_right = (center[0]-distance_to_avoid,center[1]+distance_to_avoid)
    point_up_right = (center[0]+distance_to_avoid,center[1]+distance_to_avoid)
    point_up_left = (center[0]+distance_to_avoid,center[1]-distance_to_avoid)
    #Deciding from which points the route should go through
    if(destination[0]-origin[0]>0 and destination[1]-origin[1]>0):
        points = [point_bottom_left,point_bottom_right,point_up_right]
    elif(destination[0]-origin[0]<0 and destination[1]-origin[1]<0):
        points = [point_bottom_left,point_bottom_right,point_up_right]
        points.reverse()
    elif(destination[0]-origin[0]<0 and destination[1]-origin[1]>0):
        points = [point_up_left,point_bottom_left,point_bottom_right]
    elif(destination[0]-origin[0]>0 and destination[1]-origin[1]<0):
        points = [point_up_left,point_bottom_left,point_bottom_right]
        points.reverse()
    else:
        points = []

    # Download the street network data for the location
    graph = ox.graph_from_place('Dublin,Ireland', network_type='drive')
    origin_node = ox.distance.nearest_nodes(graph, origin[0], origin[1])
    destination_node = ox.distance.nearest_nodes(graph, destination[0], destination[1])

    # Create a list of node IDs corresponding to the points in the path
    nodes = [origin_node]
    for point in points:
        node = ox.distance.nearest_nodes(graph, point[0], point[1])
        nodes.append(node)
    nodes.append(destination_node)
    # Calculate the shortest path between each consecutive pair of nodes
    path = []
    for i in range(len(nodes)-1):
        start_node = nodes[i]
        end_node = nodes[i+1]
        try:
            route = nx.shortest_path(graph, start_node,end_node, weight='length')
            path.extend(route[:-1])
        except nx.NetworkXNoPath:
            print('No path between nodes:', start_node, end_node)

    # Convert the list of node IDs to a list of latitudes and longitudes
    path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]
    
    feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }
    #To change from lat and lng to lng andlat
    coordinate_list = []
    for coordinate in path_coords:
        lat, lng = coordinate
        coordinate_list.append([lng, lat])

    #To select random three location to form recommendation message
    selected_coordinates = random.sample(coordinate_list, 3)
    coordinate_list = createGeo(coordinate_list)
    coordinate_list['features'][0]['properties']['plot_type']="New route"

    #To form feature collection
    feature_collection['features'] += coordinate_list['features']
    geo = isochrome(center[0], center[1]) 
    geo['features'][0]['properties']['plot_type']="Incident plot"
    feature_collection['features'] += geo['features']

    return (feature_collection,selected_coordinates)

