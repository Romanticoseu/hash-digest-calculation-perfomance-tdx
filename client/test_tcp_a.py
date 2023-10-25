import socket

# Define the server address (host and port)
server_host = 'localhost'
server_port = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))

while True:
    message= input("Enter a message to send to the server: ")
    
    # Send the message to the server
    client_socket.send(message.encode('utf-8'))
    
    # Receive the response from the server
    data = client_socket.recv(1024)
    response = data.decode('utf-8')
    print(f"Received from the server: {response}")
    