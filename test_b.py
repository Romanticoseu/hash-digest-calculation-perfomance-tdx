import socket

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
    print(f"Received from {client_address}: {data.decode('utf-8')}")

    # You can add your processing logic here

    # Send a response back to the client
    response = "Hello from the server"
    server_socket.sendto(response.encode('utf-8'), client_address)
