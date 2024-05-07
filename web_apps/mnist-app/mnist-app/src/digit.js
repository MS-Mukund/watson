import React, { useState } from 'react';

function MNISTDigitRecognition() {
  const [selectedService, setSelectedService] = useState(''); // Initialize selected service state

  const handleFileUpload = (event) => {
    event.preventDefault(); // Prevent default form submission behavior
    const formData = new FormData(); // Create FormData object

    // Append the file to the FormData object
    formData.append('image', event.target.files[0]);

    // Append the app_name field (assuming it's a constant or retrieved data)
    formData.append('app_name', 'YOUR_APP_NAME'); // Replace with your app name

    // Append the selected service name
    formData.append('service_name', selectedService);

    // Send the form data to the server using fetch
    fetch('http://127.0.0.1:7002/receive_input', {
      method: 'POST',
      body: formData, // Pass the FormData object as the body
    })
      .then(response => {
        if (response.ok) {
          console.log('File uploaded successfully');
          console.log('Form Data: ', formData)
        } else {
          console.error('Failed to upload file');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  const handleServiceChange = (event) => {
    setSelectedService(event.target.value);
  }

  const services = ['Service A', 'Service B', 'Service C']; // Replace with your services

  return (
    <div>
      <h2>MNIST Digit Recognition</h2>
      <form encType="multipart/form-data">
        <input type="file" name="image" onChange={handleFileUpload} />
        <select value={selectedService} onChange={handleServiceChange}>
          <option value="">Select Service</option>
          {services.map(service => (
            <option key={service} value={service}>
              {service}
            </option>
          ))}
        </select>
        <input type="submit" value="Upload" />
      </form>
    </div>
  );
}

export default MNISTDigitRecognition;
