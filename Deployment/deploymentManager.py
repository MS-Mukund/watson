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
import json
import random
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread

# Kafka configuration (replace with your details)
KAFKA_BROKERS = ["localhost:9092"]
DEPLOYMENT_TOPIC = "SLAConfigDetails"
DEPLOY_TO_ENGINES_TOPIC = "Deploy_to_engines"

def consume_deployments():
    """
    Consumer thread function to listen for deployment messages.
    """
    consumer = KafkaConsumer(DEPLOYMENT_TOPIC, bootstrap_servers=KAFKA_BROKERS)
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)
    for message in consumer:
        data = json.loads(message.value)
        print("Data: ",data)
        app_name = data["app_name"]
        app_path = data["app_path"]
        app_requirements = data["app_requirements"]
        app_instances = data["app_instances"]
        services_name = data["services_name"]
        services_path = data["services_path"]
        services_requirements = data["service_requirements"]
        services_instances = data["services_instances"]
        other_services_name = data["other_services_name"]
        other_services_path = data["other_services_path"]
        other_services_requirements = data["other_services_requirements"]
        other_services_instances = data["other_services_instances"]
        processed_data = {
        "app": {
            "name": app_name,
            "path": app_path,
            "requirements": app_requirements,
            "instances": app_instances,
        },
        "services": {
            "name": services_name,
            "path": services_path,
            "requirements": services_requirements,
            "instances": services_instances,
        },
        }
        if other_services_path:
            processed_data["other_services"] = {
                "name": other_services_name,
                "path": other_services_path,
                "requirements": other_services_requirements,
                "instances": other_services_instances,
            }
        print("processed Data", processed_data)
        producer.send(DEPLOY_TO_ENGINES_TOPIC, json.dumps(processed_data).encode("utf-8"))
        print("Data Produced to Engines")

def main():
    print("deployment manager started")
    deployment_consumer_thread = Thread(target=consume_deployments)
    deployment_consumer_thread.start()

if __name__ == "__main__":
    main()

    
    
