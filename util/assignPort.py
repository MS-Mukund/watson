import socketserver

def find_available_port():
    """
    Find an available port using the socketserver module.
    """
    with socketserver.TCPServer(("localhost", 0), None) as server:
        port = server.server_address[1]
        return port