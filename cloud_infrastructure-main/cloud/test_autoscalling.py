import unittest
import requests
import json
from autoscalling import app,Server
import autoscalling as app_unit

class TestAutoscalling(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_call_for_next_server(self):
        response = self.app.get('/call_for_next_server')
        self.assertEqual(response.status_code, 500)

    def test_availableServer(self):
        response = self.app.post('/availableServer/test_server/endpoint/test_endpoint',
                                    headers={'Content-Type': 'application/json'},
                                    data=json.dumps({'total_memory': '10 GB', 'used_disk_space': '1 GB', 'total_disk_space': '10 GB'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'server_added'})

    def test_addServer(self):
        response = self.app.post('/addServer/test_server/endpoint/test_endpoint',
                                    headers={'Content-Type': 'application/json'},
                                    data=json.dumps({'total_memory': '10 GB', 'used_disk_space': '1 GB', 'total_disk_space': '10 GB'}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'failure'})

    def test_calc_weight(self):
        system_health = {'total_memory': '10 GB', 'used_disk_space': '1 GB', 'total_disk_space': '10 GB'}
        weight = app_unit.calc_weight(system_health)
        self.assertEqual(type(weight), float)

    def test_call_request(self):
        response = app_unit.call_request('test_endpoint', '/getWeight')
        self.assertEqual(response[1], 404)

    def test_send_add_server_to_lb(self):
        
        server = Server('test_server', 'test_endpoint', 0)
        response = app_unit.send_add_server_to_lb('test_endpoint', server)
        self.assertEqual(response[1], 404)

    def test_send_mod_weight_to_lb(self):
        
        server = Server('test_server', 'test_endpoint', 0)
        response = app_unit.send_mod_weight_to_lb('test_endpoint', server)
        self.assertEqual(response[1], 404)

    def test_addServer_auto(self):
        response = app_unit.addServer_auto('test_server', 0, 'test_endpoint')
        self.assertEqual(response[1], 404)

    def test_check_server_health(self):
        app_unit.up_servers = {'test_server': Server('test_server', 'test_endpoint', 0)}
        app_unit.check_server_health()
        self.assertEqual(len(app_unit.up_servers.keys()), 1)

if __name__ == '__main__':
    unittest.main()
