from flask import Flask, redirect, jsonify, request
import ipaddress
import copy
import requests
import schedule
import time
import datetime
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import pdb
logging.basicConfig(level=logging.DEBUG)
import socket
import json

app = Flask(__name__)
up_servers = {}
available_servers = {}
MY_HOSTNAME = socket.gethostname() 
MY_IP = socket.gethostbyname(MY_HOSTNAME)
load_balancer = {"end_point": "10.6.48.170"+":5000"}
JAVA_PORT = 9090
HEALTH_MONITOR_PORT = 5001
MIN_WEIGHT = 100
THRESOLD_WEIGHT = 0.5
TIME_TO_WAIT_FOR_RESPONSE = 40
MAX_WEIGHT = 0
class Server:
    def __init__(self,name,endpoint,weight=0):
        self.name = name
        self.weight = weight
        self.java_server_endpoint = endpoint+":"+str(JAVA_PORT)
        self.last_info = time.time()
        self.health_monitor_endpoint = endpoint+":"+str(HEALTH_MONITOR_PORT)

    def modPoint(self,endpoint):
        self.health_monitor_endpoint = endpoint
        return "success"
    
    def modWeight(self,weight):
        self.weight = int(weight)
        return "success"

def call_request(server_endpoint,path = "getWeight"):
    app.logger.info(f'{server_endpoint}{path}')
    
    try:
        response = requests.get("http://"+f'{server_endpoint}{path}')#, headers=headers, params=params)
    except:
        app.logger.info("error while fetching loadbalancer")
        return {'message': "failure"},404
    if(response.status_code == 200):
        return response.content,response.status_code #response.content, response.status_code
    else:
        return {'message': "failure"},response.status_code
       

def send_add_server_to_lb(load_endpoint,server):
    path = "/addLB/servername/"+server.name+"/endpoint/"+server.java_server_endpoint+"/weight/"+str(server.weight)
    response = call_request(load_balancer["end_point"],path)
    return response

def send_mod_weight_to_lb(load_endpoint,server):
    path = "/modWeight/servername/"+server.name+"/weight/"+str(server.weight)
    data,status = call_request(load_endpoint,path)
    return data,status    

def removeServer_auto(servername):
    path = "/removeLB/servername/"+servername
    data,status = call_request(load_balancer["end_point"],path)
    return data,status  

def addServer_auto(servername,weight,endpoint):

    server = Server(servername,endpoint,weight)
    up_servers[servername] = server
    data,status   = send_add_server_to_lb(load_balancer["end_point"],server)
    return data,status  


@app.route('/call_for_next_server',methods=['GET'])
def call_for_next_server():
    servername = next(iter(available_servers)) 
    server = available_servers[servername]
    app.logger.info("server "+server.name+" is chosen for autoscalling up")
    del available_servers[servername]
    response,status_code = call_request(server.health_monitor_endpoint,"/upserver/"+servername)

    data = json.loads(response.decode('utf-8'))

    if status_code == 200:
        app.logger.info("health of server"+servername+ "....................................................................................................................")
        app.logger.info(data)
        app.logger.info("....................................................................................................................")
        weight = calc_weight(data)
        status = addServer_auto(data['server_name'],weight,data['server_endpoint'])
        app.logger.info("server "+server.name+" succeeded to deploy for autoscalling")
        return status
    app.logger.info("server "+server.name+" failed to deploy for autoscalling")
    return status_code
def call_to_down_one_server():
    servername = next(iter(up_servers)) 
    server = up_servers[servername]
    app.logger.info("server "+server.name+" is chosen for autoscalling down ")
    
    response,status_code = call_request(server.health_monitor_endpoint,"/downserver/"+servername)
    data = json.loads(response.decode('utf-8'))
    if status_code == 200:
        del up_servers[servername]
        available_servers[servername] = server
        status = removeServer_auto(servername)
        app.logger.info("server "+server.name+" succeeded to down server for autoscalling")
        return status
    app.logger.info("server "+server.name+" failed to deploy for autoscalling")
    return status_code


def check_server_health():
    value_min = 0
    value_max = 0
    total_servers = len(up_servers.keys())
    temp_up = copy.deepcopy(up_servers)
    for servername in temp_up:
        server = up_servers[servername]
        if ((time.time() - server.last_info)> TIME_TO_WAIT_FOR_RESPONSE):
            response = call_request(server,"/status/java")
            try:
                if response.status_code != 200:
                    app.logger.info("....................................................................................................................")
                    app.logger.info("server down Alert! servername:"+servername)
                    app.logger.info("....................................................................................................................")
                    del up_servers[servername]
                    continue
                else:
                    server.last_info = time.time()
            except:
                    app.logger.info("....................................................................................................................")
                    app.logger.info("server down Alert! servername:"+servername)
                    app.logger.info("....................................................................................................................")
                    del up_servers[servername]
                    continue
        if (server.weight < MIN_WEIGHT):
            value_min = value_min+1
        elif(server.weight > MAX_WEIGHT):
            value_max = value_max+1

    if(total_servers == 0 or value_min/total_servers >THRESOLD_WEIGHT):
        while (len(available_servers.keys())>0):
            app.logger.info("request sending for autoscalling up")
            status = call_for_next_server()

            if(status == 200):
                app.logger.info("autoscalling server up done...........")
                return 1
            else:
                app.logger.info("not successful to autoscale server one server, trying for another")
        app.logger.info("no server available for autoscalling")
        time.sleep(3)
        return 0
    elif(value_min/total_servers >THRESOLD_WEIGHT):
        while (len(up_servers.keys())>0):
            app.logger.info("request sending for autoscalling down")
            status = call_to_down_one_server()
            if(status == 200):
                app.logger.info("autoscalling serve down done...........")
                return 1
            else:
                app.logger.info("not successful to autoscale server one server, trying for another")
        time.sleep(3)
        return 0

    return 1
    
def calc_weight(system_health):
    ram = ( float(system_health['total_memory'].split(' ')[0])/float(system_health['total_memory'].split(' ')[0]))*100
    disk = (1-float(system_health['used_disk_space'].split(' ')[0])/float(system_health['total_disk_space'].split(' ')[0]))*100
    weight = 0.7*ram+0.3*disk
    return weight

@app.route('/availableServer/<servername>/endpoint/<endpoint>',methods=['POST'])
def availableServer(servername,endpoint):
    weight = 0
    if ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
        system_health = request.get_json()
        weight = calc_weight(system_health)
    server = Server(servername,endpoint,weight)
    available_servers[servername] = server
    
    return {"message": "server_added"},200

@app.route('/addServer/<servername>/endpoint/<endpoint>',methods=['POST'])
def addServer(servername,endpoint):
    weight = 0
    if ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
        system_health = request.get_json()
        weight = calc_weight(system_health)
    server = Server(servername,endpoint,weight)
    up_servers[servername] = server
    
    response = send_add_server_to_lb(load_balancer["end_point"],server)

    return jsonify({"message":"success"}),200

@app.route('/health/server/<servername>',methods=['POST'])
def receive_health(servername):
    server = up_servers[servername]
    server.last_info = time.time()
    app.logger.info(request.remote_addr)
    app.logger.info("received health data from "+servername+"..................................................................")
    
    if ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json' and servername in up_servers):
        system_health = request.get_json()
        app.logger.info("....................................................................................................................")
        app.logger.info("system health for server"+servername)
        app.logger.info(system_health)
        app.logger.info("....................................................................................................................")
        
        weight = calc_weight(system_health)
        # weight = server.weight+1
        if(abs(weight -server.weight)>0):
            server.weight = weight
            send_mod_weight_to_lb(load_balancer["end_point"],server)   
    return jsonify({"message":"success"}),200




if __name__ == '__main__':
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    app.logger.info("System UP")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_server_health, trigger="interval", seconds=30)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
    app.run(host="0.0.0.0",port = 5002,use_reloader=False)