from django.test import TestCase, Client
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .cab_map import getLocation, direction, createGeo
from .reroute import isochrome 
from .clustercab import location
from .tweet import deEmojify, formatTime, find_ends
from .predict_dublinbikes import predict
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class ViewSetTests(APITestCase):

    def test_getLocation(self):
        """
        Tests to get location
        """
        loc_name = "Dublin Airport"
        loc = getLocation(loc_name)
        self.assertEqual(loc, "-6.2567915, 53.424077499999996")

        loc_name = "Trinity College Dublin"
        loc = getLocation(loc_name)
        self.assertEqual(loc, "-6.2578510000000005, 53.344310500000006")

        loc_name = "Grafton Street, Dublin"
        loc = getLocation(loc_name)
        self.assertEqual(loc,"-6.260301, 53.3414175")
    
    def test_direction(self):
        """
        Tests to get direction
        """
        start = "-6.243, 53.427"
        end = "-6.260177, 53.342593"
        data = direction(start, end)
        self.assertEqual(data['routes'][0]['distance'], 15223.09)
        self.assertEqual(data['routes'][0]['duration'], 1559.253)
        self.assertEqual(data['waypoints'][0]['name'], "Corballis Road South")
        self.assertEqual(data['waypoints'][1]['name'], "Clarendon Street")

    def test_createGeo(self):
        """
        Tests to create geo json
        """
        data = {'routes': [{'weight_name': 'auto', 'weight': 1476.285, 'duration': 1125.309, 'distance': 6573.259, 'legs': [{'via_waypoints': [], 'admins': [{'iso_3166_1_alpha3': 'IRL', 'iso_3166_1': 'IE'}], 'weight': 1476.285, 'duration': 1125.309, 'steps': [], 'distance': 6573.259, 'summary': 'Stillorgan Road, R118'}], 'geometry': {'coordinates': [[-6.220262, 53.307014], [-6.220437, 53.307094], [-6.219362, 53.307617], [-6.218896, 53.308639], [-6.219956, 53.309296], [-6.219019, 53.309581], [-6.222217, 53.313222], [-6.226728, 53.315287], [-6.232028, 53.31918], [-6.230149, 53.322213], [-6.231242, 53.325784], [-6.23066, 53.328571], [-6.230764, 53.328977], [-6.234965, 53.331818], [-6.238135, 53.336142], [-6.240599, 53.337674], [-6.239066, 53.338696], [-6.246187, 53.34138], [-6.246426, 53.343527], [-6.255021, 53.345218], [-6.255, 53.34749], [-6.263678, 53.345929]], 'type': 'LineString'}}], 'waypoints': [{'distance': 21.939, 'name': '', 'location': [-6.220262, 53.307014]}, {'distance': 47.704, 'name': 'Wellington Quay', 'location': [-6.263678, 53.345929]}], 'code': 'Ok', 'uuid': 'lE1zFqUl4lY0FBdfsoGk__edcLP1YsDPKuOKnvj4T0aCTHhZJq_j4Q=='}
        feature_collection = createGeo(data)
        self.assertEqual(feature_collection['features'][0]['geometry']['coordinates'],[[-6.220262, 53.307014],[-6.220437, 53.307094],[-6.219362, 53.307617],
        [-6.218896, 53.308639],[-6.219956, 53.309296],[-6.219019, 53.309581],[-6.222217, 53.313222],[-6.226728, 53.315287],[-6.232028, 53.31918],[-6.230149, 53.322213],
        [-6.231242, 53.325784],[-6.23066, 53.328571],[-6.230764, 53.328977],[-6.234965, 53.331818],[-6.238135, 53.336142],[-6.240599, 53.337674],[-6.239066, 53.338696],
        [-6.246187, 53.34138],[-6.246426, 53.343527],[-6.255021, 53.345218],[-6.255, 53.34749],[-6.263678, 53.345929]])
        self.assertEqual(feature_collection['features'][0]['properties']['distance'], 6573.259)
        self.assertEqual(feature_collection['features'][0]['properties']['duration'], 1125.309)
        self.assertEqual(feature_collection['features'][0]['properties']['waypoints'], ['', 'Wellington Quay'])


    def test_geojson(self):
        """
        Test to get geojson data
        """

        url = 'http://127.0.0.1:8000/geojson/'
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_isochrom(self):
        """
        Test to get iscochrome data
        """
        loc = isochrome("-6.243","53.427")
        self.assertEqual(loc,{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[-6.244, 53.428124], [-6.244013, 53.426987], [-6.243, 53.426957], [-6.243913, 53.427087], [-6.244, 53.428124]]}, 'properties': {}}]})

    def test_Location(self):
        """
        Tests to get location name
        """
        loc_name = "Dublin Airport (DUB), Corballis Rd, Dublin, County Dublin K67, Ireland"
        loc = location(["53.424077499999996","-6.2567915"])
        self.assertEqual(loc, loc_name)

        loc_name = "Trinity College, College Green, Dublin, D02, Ireland"
        loc = location(["53.344310500000006","-6.2578510000000005"])
        self.assertEqual(loc, loc_name)

        loc_name = "Grafton Street, Sráid Grafton, Dublin, D02, Ireland"
        loc = location(["53.3414175","-6.260301"])
        self.assertEqual(loc,loc_name)


    def test_deEmojify(self):
        """
        Tests to get text without emoji
        """
        text = '⚠ Finglas ⚠\nThere is a collision on the Finglas Roundabout (Lidl). Delays building on the inbound approach from the N2, and especially on St Margaret\'s Road.'
        loc = deEmojify(text)
        self.assertEqual(loc, " Finglas \nThere is a collision on the Finglas Roundabout (Lidl). Delays building on the inbound approach from the N2, and especially on St Margaret\'s Road.")

    def test_formatTime(self):
        """
        Tests to get time and date
        """
        dt = datetime(2022, 4, 1, 12, 30, 0)
        result = formatTime(dt)
        expected_output = '12:30:00 04/01/2022'
        self.assertEqual(result, expected_output)
    
    def test_find_ends(self):
        """
        Tests to get the end of the texts
        """
        text = "Take the red line from Connolly to Tallaght via Abbey St."
        expected_output = ['Take the red line from Connolly', 'Tallaght via Abbey St.']
        self.assertEqual(find_ends(text), expected_output)
        
        text = "Take the green line from St. Stephen's Green to Sandyford"
        expected_output = ["Take the green line from St. Stephen's Green", 'Sandyford']
        self.assertEqual(find_ends(text), expected_output)
        
        text = "Take the bus from Blanchardstown to Dublin Airport"
        expected_output = ['Take the bus from Blanchardstown', 'Dublin Airport']
        self.assertEqual(find_ends(text), expected_output)

    def test_find_ends(self):
        """
        Tests to get dublin bikes prediction
        """
        json_ = {'NewTime': 23070.0, 'STATION ID': 1, 'day_of_week_int': 3, 'prev_hour_data': 6}
        pred = predict(json_)
        self.assertEqual(pred, 7)

    def setUp(self):
        self.client = APIClient()

    def test_tweet(self):
        """
        Tests to tweet api call
        """
        response = self.client.get('/tweet/')  # Replace 'your-endpoint' with the actual endpoint for the Tweet view
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_geo_json(self):
        """
        Tests to geojson api call
        """
        response = self.client.get('/geojson/')  # Replace 'your-endpoint' with the actual endpoint for the showGeoJson view
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_traffic(self):
        """
        Tests to traffic api call
        """
        test_id = 1  # Replace this with a valid ID for testing
        response = self.client.get(f'/traffic/{1}/')  # Replace 'your-endpoint' with the actual endpoint for the returnTraffic view
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_prediction_dublin_bikes(self):
        """
        Tests to prediction api call
        """
        test_id = 1  # Replace this with a valid ID for testing
        response = self.client.get(f'/prediction/{1}/')  # Replace 'your-endpoint' with the actual endpoint for the predictionDublinBikes view
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_cluster_cab(self):
        """
        Tests to clustercab api call
        """
        test_data = {"taxis": [{"name": "taxi 1", "lon": -6.242248, "lat": 53.431226}, {"name": "taxi 2", "lon": -6.265379, "lat": 53.324035}, {"name": "taxi 3", "lon": -6.258212, "lat": 53.344284}, {"name": "taxi 4", "lon": -6.242248, "lat": 53.431226}, {"name": "taxi 5", "lon": -6.258782, "lat": 53.344197}, {"name": "taxi 6", "lon": -6.265956, "lat": 53.343473}, {"name": "taxi 7", "lon": -6.265379, "lat": 53.324035}, {"name": "taxi 8", "lon": -6.220437, "lat": 53.307094}, {"name": "taxi 9", "lon": -6.252127, "lat": 53.341627}, {"name": "taxi 10", "lon": -6.313622, "lat": 53.34235}, {"name": "taxi 11", "lon": -6.258212, "lat": 53.344284}, {"name": "taxi 12", "lon": -6.303378, "lat": 53.353851}, {"name": "taxi 13", "lon": -6.220437, "lat": 53.307094}, {"name": "taxi 14", "lon": -6.313622, "lat": 53.34235}, {"name": "taxi 15", "lon": -6.242248, "lat": 53.431226}, {"name": "taxi 16", "lon": -6.312609, "lat": 53.342342}, {"name": "taxi 17", "lon": -6.265379, "lat": 53.324035}, {"name": "taxi 18", "lon": -6.313622, "lat": 53.34235}, {"name": "taxi 19", "lon": -6.265614, "lat": 53.340671}, {"name": "taxi 20", "lon": -6.265614, "lat": 53.340671}]}  # Replace this with valid data for testing
        response = self.client.post('/clustercab/', data=test_data, format='json')  # Replace 'your-endpoint' with the actual endpoint for the returnClusterCab view
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
