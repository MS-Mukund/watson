from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import sys
import requests
# mnist model import
from keras.datasets import mnist
from keras.models import load_model
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# URL is taken as an argument
URL = '/predict'
url_infer = 'http://127.0.0.1:6000/receive_output'

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
    ])

# Define a function to preprocess input image
def preprocess_image(image):
    # Reshape the image to 28x28 and normalize pixel values
    image = np.array(image, dtype=np.float32)
    image = image.reshape((1, 28, 28, 1))
    image /= 255.0
    return image

@app.route('/predict', methods=['POST'])
def predict():
    # Get image data from request
    image_data = request.files['image'].read()
    image = tf.image.decode_png(image_data, channels=1)
    # image = preprocess_image(image)
    
    # Make prediction
    prediction = model
    
    # Get the predicted digit
    predicted_digit = np.argmax(prediction)
    
    data = jsonify({'predicted_digit': str(predicted_digit)})
    send_output(url_infer,data)
    return data
    
def send_output(url,data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data sent successfully to URL")
        else:
            print("Failed to send data to URL:", response.status_code)
    except Exception as e:
        print("Exception occurred while sending data to URL:", str(e))


@app.route('/display', methods=['POST'])
def display():
    return request.json

if __name__ == '__main__':      
    # Load the MNIST model
    (train_X, train_y), (test_X, test_y) = mnist.load_data()
    
    ds_train = tf.data.Dataset.from_tensor_slices((train_X, train_y))
    ds_train = ds_train.shuffle(60000).batch(32)
    ds_test = tf.data.Dataset.from_tensor_slices((test_X, test_y))
    ds_test = ds_test.batch(32)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    model.fit(
        ds_train,
        epochs=6,
        validation_data=ds_test,
    )
    
    app.run(debug=True, port=6001)
    