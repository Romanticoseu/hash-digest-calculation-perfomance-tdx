import socket
import os

# Define the server address (host and port)
server_host = os.getenv("SERVER_HOST_NAME")  # Change this to the IP of the server
server_port = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message to send to the server: ")

    # Send the message to the server
    client_socket.sendto(message.encode('utf-8'), (server_host, server_port))

    # Receive the response from the server
    response, server_address = client_socket.recvfrom(1024)
    print(f"Received from {server_address}: {response.decode('utf-8')}")
