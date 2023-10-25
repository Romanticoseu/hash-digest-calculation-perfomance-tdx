import socket
import hashlib

# Define the server address (host and port)
server_host = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

print(f"Server listening on {server_host}:{server_port}")

while True:
    # Receive data from the client
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Received from {client_address}: {message}")

    # Calculate the SHA-256 hash of the message
    sha256_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"SHA-256 Hash: {sha256_hash}")

    # Send the hash back to the client
    server_socket.sendto(sha256_hash.encode('utf-8'), client_address)
