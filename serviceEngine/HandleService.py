def redirect(service, path):
    # call the service given the path
    status, error = service(path)
    if( status == "success"):
        print("Service executed successfully")
    else:
        print("Service error: ", error)
    
    return status
        