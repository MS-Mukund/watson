from kafka import KafkaProducer, KafkaConsumer
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
def send_input_to_url(data):
    try:
        response = requests.post('http://127.0.0.1:6001/predict', json=data)
        if response.status_code == 200:
            print("Data sent successfully to URL")
        else:
            print("Failed to send data to URL:", response.status_code)
    except Exception as e:
        print("Exception occurred while sending data to URL:", str(e))

@app.route('/receive_output', methods=['POST'])
def receive_output():
    data = request.json
    print("Received data:", data)    
    # Check if data is received
    if data is not None:
        data_str = json.dumps(data)
        kafka_producer.produce("output", value=data_str)
        kafka_producer.flush()
        return "Data received and sent to Kafka successfully", 200
    else:
        return "No data received", 400 

def kafka_consumer():
    consumer = KafkaConsumer('input', bootstrap_servers='localhost:9092')
    for message in consumer:
        try:
            data = json.loads(message.value.decode('utf-8'))
            send_output_to_url(data)
        except Exception as e:
            print("Error processing message:", str(e))

if __name__ == "__main__":
    import threading
    consumer_thread = threading.Thread(target=kafka_consumer)
    consumer_thread.start()
    app.run(port=6000)
    

