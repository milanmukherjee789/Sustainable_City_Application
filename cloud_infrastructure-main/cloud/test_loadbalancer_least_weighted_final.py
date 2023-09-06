import unittest
from loadbalancer_least_weighted_final import app, Loadbalancer, Server
import json

import socket
MY_HOSTNAME = socket.gethostname() 
MY_IP = socket.gethostbyname(MY_HOSTNAME)
lb = Loadbalancer()
class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server("server1", 1, "http://localhost:8080")

    def test_server_init(self):
        server = self.server
        self.assertEqual(server.name, "server1")
        self.assertEqual(server.weight, 1.0)
        self.assertEqual(server.endpoint, "http://localhost:8080")
        self.assertEqual(server.connection, 1)

    def test_server_mod_point(self):
        server = self.server
        res, code = server.modPoint("http://localhost:8081")
        self.assertEqual(res["message"], "success")
        self.assertEqual(code, 200)
        self.assertEqual(server.endpoint, "http://localhost:8081")

    def test_server_mod_weight(self):
        server = self.server
        res, code = server.modWeight(2)
        self.assertEqual(res["message"], "success")
        self.assertEqual(code, 200)
        self.assertEqual(server.weight, 2.0)

class TestLoadBalancer(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        
    def test_add_server(self):
        
        lb.addServer('testserver', Server('testserver', 2, MY_IP))
        response = self.client.get('/addLB/servername/testserver/endpoint/'+MY_IP+'/weight/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        self.assertIn('testserver', lb.getServers())
        

        
    def test_modify_endpoint(self):
        lb.modserver_endpoint('testserver',MY_IP)
        response = self.client.get('/modEndpoint/servername/testserver/endpoint/'+MY_IP)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        self.assertEqual(lb.getServers()['testserver'].endpoint, MY_IP)
        
    def test_modify_weight(self):
        lb.modserver_weight('testserver', 3)
        response = self.client.get('/modWeight/servername/testserver/weight/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        self.assertEqual(lb.getServers()['testserver'].weight, 3)
    def test_remove_server(self):
        lb.removeServer('testserver')
        response = self.client.get('/removeLB/servername/testserver')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        self.assertNotIn('testserver', lb.getServers())    
    def test_forward_request(self):
        lb.addServer('testserver1', Server('testserver1', 2, MY_IP))
        lb.addServer('testserver2', Server('testserver2', 3, MY_IP))
        response = self.client.get('/test', headers={'Host': MY_IP})
        self.assertEqual(response.status_code, 404)  # No server available
        
    def test_forward_request_with_valid_path(self):
        lb.addServer('testserver1', Server('testserver1', 2, MY_IP))
        lb.addServer('testserver2', Server('testserver2', 3, MY_IP))
        response = self.client.get('/test', headers={'Host': MY_IP+':5000'})
        
        self.assertEqual(response.status_code, 404)  # No server available


        
    # def test_breakpoint(self):
    #     response = self.client.get('/breakpoint')
    #     self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()



