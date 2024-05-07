import React, { useState, useEffect } from 'react';

function MNISTDigitRecognition() {
    const [url, setUrl] = useState("http://localhost:7002/receive_input");
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedService, setSelectedService] = useState("");

    useEffect(() => {
        const webEngineUrl = process.env.REACT_APP_WEB_ENGINE_URL;
        if (webEngineUrl) {
            setUrl(webEngineUrl);
        }
    }, []);

    function handleFileSelect(event) {
        const file = event.target.files[0]; // Access event target properly
        setSelectedFile(file);
    };

    function handleFileUpload(event) {
        event.preventDefault(); // Prevent default form submission
        if (!selectedFile) return; // Handle case where no file is selected

        const formData = new FormData();
        console.log("Selected File: ", selectedFile);
        console.log("Selected Service: ", selectedService);
        
        formData.append('image', selectedFile);
        formData.append('app_name', 'YourAppNameHere');
        formData.append('service_name', selectedService);
        console.log("Form Data: ", formData);

        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                alert("inside if");
                console.log('File uploaded successfully');
                console.log("service name: ", formData.get('service_name'));
                console.log("app_name: ", formData.get('app_name'));
                console.log("Form Data: ", formData);
            } else {
                alert("in else");
                console.error('Failed to upload file');
            }
        })
        .catch(error => {
            alert("caught the error");
            alert(error);
            console.error('Error:', error);
            // print status code
            console.log("status code: ", error.response.status);
        });
    };

    function handleServiceChange(event) {
        setSelectedService(event.target.value);
    };

    return (
        <div>
            <h2>MNIST Digit Recognition</h2>
            <form onSubmit={handleFileUpload} encType="multipart/form-data">
                <input type="file" name="image" onChange={handleFileSelect} />
                <select value={selectedService} onChange={handleServiceChange}>
                    <option value="">Select a service</option>
                    <option value="Service1">Service 1</option>
                    <option value="Service2">Service 2</option>
                    <option value="Service3">Service 3</option>
                </select>
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}

export default MNISTDigitRecognition;
