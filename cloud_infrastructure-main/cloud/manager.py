import psutil
import shutil
from flask import Flask, redirect, request,jsonify


import os
import schedule
import time
import datetime
import ipaddress
import requests
import socket
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import pdb
import subprocess


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

JAVA_PORT = 9090
HEALTH_MONITOR_PORT = 5001
AUTOSCALING_SERVER_PORT = 5002

MY_HOSTNAME = socket.gethostname() 
MY_IP = socket.gethostbyname(MY_HOSTNAME)
AUTOSCALING_SERVER = {"endpoint": "10.6.62.168"}

def get_system_health():
    memory_stats = psutil.virtual_memory()
    total_memory = memory_stats.total
    used_memory = memory_stats.used
    free_memory = memory_stats.available

    disk_stats = shutil.disk_usage('/')
    total_disk_space = disk_stats.total
    used_disk_space = disk_stats.used
    free_disk_space = disk_stats.free
    
    cpu_usage = psutil.cpu_percent()

    uptime = psutil.boot_time()

    total_memory_mb = total_memory / (1024 * 1024)
    used_memory_mb = used_memory / (1024 * 1024)
    free_memory_mb = free_memory / (1024 * 1024)
    total_disk_space_gb = total_disk_space / (1024 * 1024 * 1024)
    used_disk_space_gb = used_disk_space / (1024 * 1024 * 1024)
    free_disk_space_gb = free_disk_space / (1024 * 1024 * 1024)

    system_health = {
        'status': check_app_Server_status(),
        'server_name': MY_HOSTNAME,
        'server_endpoint' : MY_IP,
        'total_memory': f'{total_memory_mb:.2f} MB',
        'used_memory': f'{used_memory_mb:.2f} MB',
        'free_memory': f'{free_memory_mb:.2f} MB',
        'total_disk_space': f'{total_disk_space_gb:.2f} GB',
        'used_disk_space': f'{used_disk_space_gb:.2f} GB',
        'free_disk_space': f'{free_disk_space_gb:.2f} GB',
        'cpu_usage': f'{cpu_usage:.2f}%'
    }
    return system_health
def schedule_health_send():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_health, trigger="interval", seconds=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return 1
def check_app_Server_status():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = sock.connect_ex((MY_IP, JAVA_PORT))
    if status == 0:
        return "up"
    else:
        return "down"

@app.route('/upserver/<servername>')
def upServer(servername):
    if(check_app_Server_status() == "down"):
        subprocess.Popen(["python", "sample_webserver.py"],creationflags=subprocess.CREATE_NEW_CONSOLE)
    schedule_health_send()  
    # subprocess.Popen(["java", "-jar", "/path/to/springboot/app.jar"])
    return get_system_health(),200


@app.route('/downserver/<servername>')
def downServer(servername):
    cmd = "git --version"
    value = os.system(cmd)
    app.logger.info(value)
    return {"message":"down"},200

@app.route('/status/<servername>')
def statusServer(servername):    
    app.logger.info("status server called")

    status = check_app_Server_status()
    return {"message":status},200


def post_request(server_endpoint,port,path,my_health = {}):
    print("send request to : http://"+f'{server_endpoint}:{port}{path}')
    try:
        response = requests.post("http://"+f'{server_endpoint}:{port}{path}', json=my_health)
    except:
        with app.app_context():
            response = jsonify({"message":"failure"})
            response.status_code = 404
            response.ok = False

    print(response)
    return response

def send_health():
    app.logger.info("preparing to send health data")
    system_health = get_system_health()
    
    app.logger.info("health data sent")
    response = post_request(AUTOSCALING_SERVER['endpoint'],AUTOSCALING_SERVER_PORT,'/health/server/'+MY_HOSTNAME,my_health = system_health)
    return response

@app.route('/breakpoint')
def break_here():
    breakpoint()
    return "abcd",200

import socket
def add_java_server_to_as():
    app.logger.info("checking for java server")
    my_health = get_system_health()
    java_server_port = JAVA_PORT
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    result = sock.connect_ex((MY_IP, JAVA_PORT))
    if(result == 0):
        app.logger.info("System UP.....JAVA Server UP")
        app.logger.info("Sent data to Autoscalling Server")
        res = post_request(AUTOSCALING_SERVER['endpoint'],AUTOSCALING_SERVER_PORT,'/addServer/'+MY_HOSTNAME+'/endpoint/'+MY_IP,my_health)
        schedule_health_send()
    else:
        app.logger.info("System UP........JAVA Server not UP")
        app.logger.info("Sent data to Autoscalling Server")
        res = post_request(AUTOSCALING_SERVER['endpoint'],AUTOSCALING_SERVER_PORT,'/availableServer/'+MY_HOSTNAME+'/endpoint/'+MY_IP,my_health)
    app.logger.info("autoscale server returned response ")
    if res and res.ok:
        
        app.logger.info(res.json())
    else:
        app.logger.error("error from autoscale server")
    return res
            

if __name__ == '__main__':

    app.logger.info("System UP")
    
    add_java_server_to_as()
    
    app.run(host="0.0.0.0",port = 5001,use_reloader=False)
