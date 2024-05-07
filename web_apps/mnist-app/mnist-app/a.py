import os
import subprocess
import socket

def give_available_port(start_port=3024, end_port=49151):
    """
    Finds an available port within a specified range.

    Args:
        start_port (int, optional): The starting port number for searching (default 1024).
        end_port (int, optional): The ending port number for searching (default 49151).

    Returns:
        int: An available port number, or None if no port is found.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for port in range(start_port, end_port + 1):
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                pass
              
    return None

def serve_react_app(path):
    print('1 inside serve_react_app')
    # Get an available port and set environment variable for React app
    available_port = give_available_port()
    print('2 found port: ', available_port)
    os.environ['PORT'] = str(available_port)

    print('3 before chdir')
    # Check if requested path matches a React app
    os.chdir(f"{path}")
    subprocess.Popen(["npm", "install"])
    subprocess.Popen(["npm", "start"])
        
    return available_port


print('started main')
serve_react_app('./')
print('end of serve_react_app')