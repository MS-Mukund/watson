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
