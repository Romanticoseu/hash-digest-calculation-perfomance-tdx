import socket
import hashlib

# Define the server address (host and port)
server_host = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(5)  # Maximum number of queued connections

print(f"Server listening on {server_host}:{server_port}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Receive data from the client
    data = client_socket.recv(1024)
    message = data.decode('utf-8')
    print(f"Received from {client_address}: {message}")

    # Calculate the SHA-256 hash of the message
    sha256_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"SHA-256 Hash: {sha256_hash}")

    # Send a response back to the client
    response = sha256_hash
    client_socket.send(response.encode('utf-8'))


