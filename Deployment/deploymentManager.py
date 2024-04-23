'''
Deployment manager - Takes file paths of 
inference service and web app service from packaging tools
sends kafka message to inference engine and webapp engine
kafka. Assigns an instance ID to the running app: {
instancd_id: 'INSTANCE_ID',
file_path: 'path/to/file'
}

Starts the web app and inference services (directory paths provided in the config file)
Runs the main script of the file(is this done?). 
Assigns port to web app and inference services. 
Redirect URL also must be assigned.  
'''
import os
import json

from kafka import KafkaProducer
from runtime.nodeManager import NodeManager

def deployApp(message):
    pass
    
    
