''' 
Developer designs an app with components: 
- Webapp (takes input from end user)
- Inference (takes input from webapp and returns output)

Our task is to develop a webEngine that takes input from webapp, converts it to
kafka message, and sends it to inference engine. Inference engine will convert 
it back to a HTTP request and send it to the inference service. 

The developer is required to send the HTTP request from the webapp via a URL
which is taken as an argument (we will provide our webEngine URL as an argument
during deployment). 
Similarly, the inference engine will send the HTTP request to the inference
service via a URL which is taken as an argument.  
'''
from kafka import KafkaProducer, KafkaConsumer
import json
import requests
from flask import Flask, request,render_template

import base64
from flask_cors import CORS

import threading
import time

import subprocess

# def img_to_json(img):
    
app = Flask(__name__)
cors = CORS(app)

import logbook
logbook.set_datetime_format("local")

# import sys
# sys.path.append('..')
# from logs.logger import setup_logger

'''
The endpoint url is addded to the HTTP json request (field is destination). 
Instead of endpoint URL, the url field is set to webEngine URL.
destination: URL
url: webEngine

If this doesn't work, use nginx as proxy server to redirect all URLs to webEngine
'''
'''
ignore this for now
The endpoint url is addded to the HTTP json request (field is destination). 
Instead of endpoint URL, the url field is set to webEngine URL.
destination: URL
url: webEngine

If this doesn't work, use nginx as proxy server to redirect all URLs to webEngine
'''

'''
kafka_msg = {
    "app_name": <app_name>,
    "num_instances": Int
    }
after receiving the message from DEPLOY_TO_ENGINES_TOPIC topic, 
dynamically assigns a port to each instance of react app and runs them, 
(maybe it's better to store the: app_name, app_ID, port in a file)

Now, send a message to "web_deployment_toinf" topic with: 
{"app_ID": <app_ID>, "app_name": <app_name>}
  
later: final output should be displayed in the same webpage, not redirected to backend. 
'''
KAFKA_BROKERS = ["localhost:9092"]
DEPLOY_TO_ENGINES_TOPIC = "Deploy_to_engines"

destination_url = 'http://127.0.0.1:6001/display'
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

from flask import Flask, render_template, send_from_directory
import socket  # For finding available port
import os
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__)


# Database connection
uri = "mongodb+srv://bokkagaru:paadugajala@cluster0.tr0pl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("Web_Engine")
# relative imports
sys.path.append('..')
from util.createEnv import create_env_and_install
from util.runApp import run_app
from util.assignPort import give_available_port

PORT = 7002

def serve_react_app(path):
    # Get an available port and set environment variable for React app
    available_port = give_available_port()
    os.environ['PORT'] = str(available_port)

    # Check if requested path matches a React app
    os.chdir(f"{path}")
    subprocess.Popen(["npm", "install"])
    subprocess.Popen(["npm", "start"])
    os.environ['REACT_APP_WEB_ENGINE_URL'] = f"http://localhost:{PORT}/receive_input"
        
    return available_port

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
        app_path = app_data.get("path")
        app_requirements = app_data.get("requirements")
        app_instances = app_data.get("instances")
        if app_path:
            print(f"App Path: {app_path}")
        if app_requirements:
            print(f"App Requirements: {app_requirements}")
        if app_instances:
            print(f"App Instances: {app_instances}")   
        
        # instance_id(created by app_name
        for _ in range(app_instances):
            avbl_port = serve_react_app(app_path) 
                   
            data = {
                "app_name": app_name,
                "app_path": app_path,
                "port": avbl_port,
                "status": "running",  # Add status for better record keeping
                "PID":"pid"
            }
            collection = db["Web_Engine_Instances"]  # Connect to the collection
            collection.insert_one(data)
        print("-" * 40)  # Separator for readability

# destination_url = 'http://127.0.0.1:6001/display'
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
@app.route('/receive_input', methods=['POST'])
def receive_input():
    print('start of receive_input()')
    t_stamp = time.time()
    if len(request.files) == 0:
        return "No data received", 400

    # Iterate through each file in the request
    print('before for', request.files['image'].filename)
    print('service_name: ', request.form.get('service_name'))
    print('app_name: ', request.form.get('app_name'))
    print(request)
    for file_key, file_obj in request.files.items():
        # Determine the type of the file
        print('file_key: ', file_key, file_obj.filename, file_obj)
        file_type = determine_file_type(file_obj.filename)
        # Process the file based on its type
        if file_type == 'image':
            print('before process_image')
            process_image(file_obj,t_stamp, request.form.get('app_name'),request.form.get('service_name'))
        elif file_type == 'audio':
            process_audio(file_obj)
        elif file_type == 'text':
            process_text(file_obj)
        else:
            # Unsupported file type
            print(file_type)
            return f"Unsupported file type: {file_type}", 400
    predicted = None
    consumer = KafkaConsumer('output', bootstrap_servers='localhost:9092',auto_offset_reset='earliest')
    print("start of kafka_consumer()")
    for message in consumer:
        #print("message: ",message)
        try:
            #print("entering try block")
            data = json.loads(message.value.decode('utf-8'))
            if data["tstamp"] == t_stamp:
                print("final frontier ", data["data"], type(data["data"]) )
                predicted = data["data"]
                return str(predicted), 200
                
        except KeyError:
            pass
        except Exception as e:
            print("Error processing message:", str(e))
        
        
    consumer.close()    
    
    return predicted, 200

def determine_file_type(filename):
    print('start of determine_file_type()', filename)
    # Simple logic to determine the file type based on the file extension
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return 'image'
    elif filename.lower().endswith(('.wav', '.mp3', '.ogg')):
        return 'audio'
    elif filename.lower().endswith(('.txt', '.csv')):
        return 'text'
    else:
        return 'unknown'

def process_image(image_file, t_stamp, app_name,service_name):
    print('start of process_image()')
    # Read the image data and encode it as base64
    image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    print('before kafka sending')
    # Send the base64 encoded image data to Kafka
    request = {"data": base64_image,"tstamp":t_stamp, "app_name": app_name,"service_name": service_name}

    kafka_producer.send("input", value=json.dumps(request).encode('utf-8'))
    print('before flush')
    kafka_producer.flush()

    print("Image data sent to Kafka successfully")

def process_audio(audio_file):
    # Read the audio data and encode it as base64
    audio_data = audio_file.read()
    base64_audio = base64.b64encode(audio_data).decode('utf-8')

    # Send the base64 encoded audio data to Kafka
    kafka_producer.send("input", value=base64_audio.encode('utf-8'))
    kafka_producer.flush()

    print("Audio data sent to Kafka successfully")

def process_text(text_file):
    # Read the text data
    text_data = text_file.read().decode('utf-8')

    # Send the text data to Kafka
    kafka_producer.send("input", value=text_data.encode('utf-8'))
    kafka_producer.flush()

    print("Text data sent to Kafka successfully")

def send_output_to_url(data):
    print('start of send_output_to_url()', data)
    try:
        print("before sending data to URL ", data)
        response = requests.post(destination_url, json=data)
        return response
    except: 
        print("Error sending data to URL")
        return
    

# Example usage:
if __name__ == "__main__":
    # logbook
    # logger = setup_logger("../central_log.log")
    # print("WebEngine started")
    # logger.info("WebEngine started 2")
    # logger.info("WebEngine started 3")

  
    app.run(port=PORT)
    