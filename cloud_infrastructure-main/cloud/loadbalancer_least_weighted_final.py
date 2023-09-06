import random
from flask import Flask, redirect, request,jsonify
import ipaddress
import requests

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class Server:
    def __init__(self,name,weight,endpoint):
        self.name = name
        self.weight = float(weight)
        self.endpoint = endpoint
        self.connection = 1

    def modPoint(self,endpoint):
        self.endpoint = endpoint
        return {"message":"success"} ,200
    def modWeight(self,weight):
        self.weight = float(weight)
        return {"message":"success"} , 200

class Loadbalancer:
    def __init__(self,network = "a.b.c.d"):
        self.ip_network = network
        self.servers = {}
    def addServer(self,servername,server):
        self.servers[servername] = server
        return {"message":"success"} , 200
    def removeServer(self,servername):
        self.servers.pop(servername)
        return {"message":"success"} , 200
    def modserver_endpoint(self,servername,endpoint):
        return self.servers[servername].modPoint(endpoint)
    def modserver_weight(self,servername,weight):
        return self.servers[servername].modWeight(weight)
    def getServers(self):
        return self.servers

    # get the server with the least number of connections weighted by server weight
    def get_weighted_least_connection_server(self):
        least_weighted_connections = float("inf")
        least_weighted_conn_servers = []
        
        for servername,server in self.getServers().items():
            least_weighted_conn_servers.append(server)
            # weight = server.weight
            # if weight == 0:
            #     continue
            # weighted_connections = self.servers[servername].connection / weight
            # if weighted_connections < least_weighted_connections:
            #     least_weighted_connections = weighted_connections
            #     least_weighted_conn_servers = [server]
            # elif weighted_connections == least_weighted_connections:
            #     least_weighted_conn_servers.append(server)
        if len(least_weighted_conn_servers) == 0:
            return "no_server_available"
        return random.choice(least_weighted_conn_servers)

    # simulate requests and track connections
    def forward(self,path,server):
        server_url = "http://"+f'{server.endpoint}/{path}'
        if path == None:
            path=""
        else:
            path = "/"+path

        params = ""
        for key in request.args.keys():
            if params != "":
                params = params+"&"+key+"="+request.args[key]
            else:
                params = params+"?"+key+"="+request.args[key]
        url = server_url + params
        if('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
            data = request.get_json()
        else:
            data = ""
        url = server_url + params
        response = requests.request(
            method=request.method,
            url=url,
            headers= request.headers,
            json=data,
            stream=True
        )
        return response
        

    def forward_request(self,path):
        server = self.get_weighted_least_connection_server()
        if(server == "no_server_available"):
            app.logger.info("no server available")
            return "no server available" , 400
        server.connection += 1
        response = self.forward(path,server)
        app.logger.info(f"Request served by {server.name}, connections = {server.connection}")
        app.logger.info(f'{server.endpoint}/{path}')
        #response = requests.get("http://"+f'{server.endpoint}/{path}')#, headers=headers, params=params)
        server.connection -= 1
        return response


# Route all requests to the selected server

@app.route('/addLB/servername/<servername>/endpoint/<endpoint>/weight/<weight>',methods = ['GET'])
def addLB(servername,endpoint,weight):
    if servername in lb.servers:
        server = lb.servers[servername]
    else:
        server = Server(servername,weight,endpoint)
    return lb.addServer(servername,server)

@app.route('/removeLB/servername/<servername>',methods = ['GET'])
def removeLB(servername):
    return lb.removeServer(servername)

@app.route('/modEndpoint/servername/<servername>/endpoint/<endpoint>',methods = ['GET'])
def modEndpoint(servername,endpoint):
    return lb.modserver_endpoint(servername,endpoint)

@app.route('/modWeight/servername/<servername>/weight/<weight>',methods = ['GET'])
def modWeight(servername,weight):
    return lb.modserver_weight(servername,weight)

# @app.route('/breakpoint')
# def break_here():
#     breakpoint()

@app.route('/',methods=['GET', 'POST', 'PUT', 'DELETE'], defaults={'path': ''})
@app.route('/<path:path>',methods=['GET', 'POST', 'PUT', 'DELETE'])
def forward(path):
    #remote = request.remote_addr.split(".")
    host = request.host.split(".")
    try:
        response =  lb.forward_request(path)    
        return response.content,response.status_code
    except:
        return jsonify({"action": "I am down , Knock your developer out"}),404

    # ip_network= '192.168.0.0/24'
    # ipaddress.ip_address(host) in ipaddress.ip_network(ip_network)
    #server_url = select_server()
    #return redirect(server_url + path)
lb = Loadbalancer()
if __name__ == '__main__':
    #network = "a.b.c.d"
    #lb = Loadbalancer(network)
    app.run(host="0.0.0.0")