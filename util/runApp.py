import subprocess

def run_app(app_path, port):
    """
    Runs the Python application at the specified path on the given port.

    Args:
        app_path (str): The path to the Python application file.
        port (int): The port number to use.
    """
    # Use subprocess to execute the Python file with the port argument
    command = ["python", app_path, f"--port={port}"]
    subprocess.run(command)
