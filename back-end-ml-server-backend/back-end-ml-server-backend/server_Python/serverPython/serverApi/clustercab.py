from sklearn.cluster import KMeans
import numpy as np
import warnings
import requests
# ignore warnings
warnings.filterwarnings('ignore')

#Create Geojson that can be displayed on OpenStreeMap
def createGeo(coor):
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

#Create Isochrome using MapBox API
def isochrome(longitude, latitude,meters):
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    center = f'{longitude},{latitude}'
    url = f'https://api.mapbox.com/isochrone/v1/mapbox/driving/{center}?contours_meters={meters}&'
    params = {'access_token': ACCESS_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()
    coor = createGeo(data['features'][0]['geometry']['coordinates'])
    return coor


def location(centroid):
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{centroid[1]},{centroid[0]}.json?access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    loc = response["features"][0]["place_name"]
    return loc

def calculate_density(points, k):
    kmeans = KMeans(n_clusters=k, random_state=42).fit(points)
    distances = kmeans.transform(points)
    return np.sum(np.min(distances, axis=1)) / len(points)

def find_lowest_density_cluster(data, k):
    kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
    labels = kmeans.labels_.astype(int)
    
    densities = []
    for i in range(k):
        cluster_points = np.array(data)[labels == i]
        density = calculate_density(cluster_points, 1)
        densities.append(density)
    
    lowest_density_cluster = densities.index(min(densities))
    return lowest_density_cluster


def cluster(taxi):
    data = [[d["lat"], d["lon"]] for d in taxi["taxis"]]

    k = 4
    lowest_density_cluster = find_lowest_density_cluster(data, k)
    kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
    centroids = kmeans.cluster_centers_
    highest_density = []
    for i, centroid in enumerate(centroids):
        if((centroid != centroids[lowest_density_cluster]).any()):
          highest_density.append(centroid)

    lowest_density = centroids[lowest_density_cluster]
    recommendation = "Please try to divert taxies towards "
    low = str(location(lowest_density))
    low = low.replace(", Ireland", "")
    low = low.replace(", Dublin", "")
    low = low.replace(",", "/")
    recommendation += low+ " from"
    for i in highest_density:
        high = str(location(i))
        high = high.replace(", Ireland", "")
        high = high.replace(", Dublin", "")
        high = high.replace(",", "/")
        recommendation += " "+high+ ", "  
    recommendation = recommendation[:recommendation.rfind(",")] + "."

    feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }

    low_geo = isochrome(lowest_density[1],lowest_density[0],100) 
    low_geo['features'][0]['properties']['cluster_type']='Low Density cluster'
    feature_collection['features'] += low_geo['features'] 
    
    j = 1
    for i in highest_density:
        high_geo = isochrome(i[1],i[0],500)
        high_geo['features'][0]['properties']['cluster_type']='High Density cluster '+ str(j)
        feature_collection['features'] += high_geo['features']
        j = j + 1

    feature_collection['message']= recommendation 
    feature_collection['location'] = str(location(lowest_density))
    feature_collection['incident'] = "Less cab density found at location"
    return feature_collection
