import socket
import hashlib
import time

# Define the server address (host and port)
server_host = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

# Increase the buffer size for receiving data
buffer_size = 1024

print(f"Server listening on {server_host}:{server_port}")

while True:
    # Receive data from the client
    data, client_address = server_socket.recvfrom(buffer_size)

    # Record server receive time
    server_receive_time = time.time()

    message = data.decode('utf-8')
    print(f"Received from {client_address}: {message}")

    # Calculate the SHA-256 hash of the message
    hash_start_time = time.perf_counter()  # Record hash calculation start time
    sha256_hash = hashlib.sha256(message.encode()).hexdigest()
    hash_end_time = time.perf_counter()  # Record hash calculation end time
    print(f"SHA-256 Hash: {sha256_hash}")

    # Send the hash back to the client
    server_socket.sendto(sha256_hash.encode('utf-8'), client_address)

    # Calculate and print times
    print(f"Server receive time: {server_receive_time}")
    print(f"Hash calculation time: {hash_end_time - hash_start_time}")
