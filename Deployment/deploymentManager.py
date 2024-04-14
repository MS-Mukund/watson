'''
Deployment manager - takes file paths of 
inference service and web app service from packaging tools
sends kafka message to inference engine and webapp engine
kafka: {
app_id: 'APP_ID',
file_path: 'path/to/file'
}
'''