import unittest
from flask import Flask, jsonify, make_response
from manager import app
import manager as app_unit
import socket


MY_HOSTNAME = socket.gethostname() 
MY_IP = socket.gethostbyname(MY_HOSTNAME)

class Testapp_unit(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()    

    def test_get_system_health(self):
        health = app_unit.get_system_health()
        self.assertIsNotNone(health)
        self.assertIsInstance(health, dict)
        self.assertIn('server_name', health)
        self.assertIn('server_endpoint', health)
        self.assertIn('total_memory', health)
        self.assertIn('used_memory', health)
        self.assertIn('free_memory', health)
        self.assertIn('total_disk_space', health)
        self.assertIn('used_disk_space', health)
        self.assertIn('free_disk_space', health)
        self.assertIn('cpu_usage', health)

    def test_upServer(self):
        response = self.app.get('/upserver/testserver')
        self.assertEqual(response.status_code, 200)

    def test_downServer(self):
        response = self.app.get('/downserver/testserver')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '{"message":"down"}\n')

    def test_statusServer(self):
        response = self.app.get('/status/testserver')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '{"message":"down"}\n')
    def test_post_request(self):
        with app.app_context():
            response = app_unit.post_request(MY_IP, 5000, '/')
            self.assertIsNotNone(response)

    def test_add_java_server_to_as(self):
        with app.app_context():
            app_unit.add_java_server_to_as()
            #self.assertEqual(response.status_code, 404)

if __name__ == '__app_unit__':
    unittest.app_unit()
