from kafka import KafkaProducer, KafkaConsumer
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

import random
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
cors = CORS(app)

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
URL = 'http://127.0.0.1:6003/predict'


import os
import sys
import base64

# relative imports
sys.path.append('..')
from util.createEnv import create_env_and_install
from util.runApp import run_app
from util.assignPort import give_available_port

KAFKA_BROKERS = ["localhost:9092"]
DEPLOY_TO_ENGINES_TOPIC = "Deploy_to_engines"
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


# Database connection
uri = "mongodb+srv://bokkagaru:paadugajala@cluster0.tr0pl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("Inference_Engine")

URL = 'http://127.0.0.1:6003/predict'

'''
kafka_msg = {
    "app_name": <app_name>,
    "app_path": <predict service path>, 
    "requirements_path": <path to requirements.txt>
    "num_instances": Int
    }
after receiving the message from "inference_deployment" topic, 
Create a python env with name 'app_name' and install the requirements using the requirements.txt file. 
Find available port and assign it to the prediction service. 
(prediction service should take take PORT as argument),  

receive the message from "web_deployment_toinf" topic:
{"app_ID": <app_ID>, "app_name": <app_name>}
create a file (config file maybe?) which contains all predict services for the app. 
Send to predict service based on some stats (random initially). 

send app_ID, prediction_result back to webEngine via "output" topic.  
'''

@app.route('/receive_output', methods=['POST'])
def receive_output():
    print('start of receive_output()')
    
    data = request.json
    print("Received data:", data, type(data))    
    # Check if data is received
    if data is not None:
        print("before send")
        kafka_producer.send("output", value=data)
        print("receive_output() before flush", data)
        kafka_producer.flush()
        print('after flush')
        return "Data received and sent to Kafka successfully receive_output()", 200
    else:
        return "No data received", 400 

def send_input_to_url(url, data):
    print('start of send_input_to_url()', data)
    try:
        response = requests.post(url=url, json=data)
        if response.status_code == 200:
            print("Data sent successfully to URL")
        else:
            print("Failed to send data to URL:", response.status_code)
    except Exception as e:
        print("Exception occurred while sending data to URL:", str(e))
def kafka_consumer():
    print("start of kafka_consumer()")
    consumer = KafkaConsumer('input', bootstrap_servers='localhost:9092')
    for message in consumer:
        print("message: ",message)
        try:
            url = URL
            data = message.value     
            print('before send_input_to_url')                  
            send_input_to_url(url, data)
        except Exception as e:
            print("Error processing message:", str(e))

def remove_port_from_url(app_url):
    match = re.search(r":\d+", app_url)
    if match:
        return app_url[:match.start()]
    else:
        return app_url

def predict_conn(requirements_path, services_path, num_instances, service_name, app_name):
    create_env_and_install(requirements_path, services_path)
    print("Python environment created and requirements installed.")
    
    for _ in range(num_instances):
        port = give_available_port()
        run_app(services_path, port)
        
        print("App running on port:", port)
        
        with open('config.txt', 'a+') as f:
            f.write(f"{service_name} {services_path} {port} running\n")   

        data = {
            "app_name": app_name,
            "service_name": service_name,
            "service_path": services_path,
            "port": port,
            "status": "running",  # Add status for better record keeping
            "PID":"pid"
        }

        # Insert data into MongoDB collection
        collection = db["Inference_Engine_Instances"]  # Connect to the collection
        collection.insert_one(data)


def consume_deployments():
    """
    Consumer thread function to listen for deployment messages and extract service information.
    """
    consumer = KafkaConsumer(DEPLOY_TO_ENGINES_TOPIC, bootstrap_servers=KAFKA_BROKERS)

    for message in consumer:
        processed_data = json.loads(message.value)
        print("Message received from Deployment Manager:")
        print("-" * 40)  # Separator for readability

        # Extract and print app information
        app_data = processed_data.get("app", {})
        app_name = app_data.get("name")
        app_instances = app_data.get("instances")
        if app_instances:
            print(f"App Instances: {app_instances}")

        # Extract and print services information
        
        services_data = processed_data.get("services", {})
        services_name = services_data.get("name")
        services_path = services_data.get("path")
        services_requirements = services_data.get("requirements")
        services_instances = services_data.get("instances")
        if services_name:
            print(f"Services Name: {services_name}")
        if services_path:
            print(f"Services Path: {services_path}")
        if services_requirements:
            print(f"Services Requirements: {services_requirements}")
        if services_instances:
            print(f"Services Instances: {services_instances}")
        
        predict_conn(requirements_path=services_requirements, services_path=services_path,
                     num_instances=services_instances, service_name=services_name)
        
        print("-" * 40)  # Separator for readability
      
from pymongo import MongoClient

# Assuming you have already established a connection to MongoDB and obtained the db object
# client = MongoClient('mongodb://localhost:27017/')
# db = client['your_database_name']

def send_to_predict():
    print("1 start of send_to_predict()")
    consumer = KafkaConsumer('input', bootstrap_servers='localhost:9092')
    for message in consumer:           # filter based on app_name
        print("2 message: ", message)
        try:
            url = None
            print("3 before filter")
            # Fetch data from MongoDB collection
            collection = db["Inference_Engine_Instances"]
            
            print('4 before json.loads')
            # convert message.value to json
            message = json.loads(message.value)
            print("message: ", message)
            
            query = {"service_name": message['app_name'], "status": "running"}
            cursor = collection.find(query)

            for doc in cursor:
                service_path = doc["service_path"]
                port = doc["port"]
                url = 'http://localhost:' + port + '/' + message['service_name']
                if random.random() < 0.5:
                    break

            print("4 after filter, url: ", url)
            if url is None:
                url = URL
                print("No app found with the given app_name and app_url")
            
            
            print("5 before send_input_to_url")
            data = json.dumps(message)
            send_input_to_url(url, data)
            print("6 after send_input_to_url")

        except Exception as e:
            print("Error processing message:", str(e))
            continue

   
if __name__ == "__main__":
    print("Starting Kafka consumer thread")
    import threading
    consumer_thread = threading.Thread(target=send_to_predict)
    consumer_thread.start()
    print("nibba rohit")
    
    # Must listen to 
    app.run(port=6005)
    