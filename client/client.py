import socket
import os
import time

# Define the server address (host and port)
# server_host = os.getenv("SERVER_HOST_NAME") 
server_host = '127.0.0.1'  # Change this to the server's IP
server_port = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Specify the path to the file containing data
data_file_path = "iris.data"

# Define the chunk size for reading and sending data
chunk_size = 1024  # You can adjust this value as needed


# Open the data file for reading
with open(data_file_path, 'rb') as data_file:
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Record transfer time start
    transfer_start_time = time.time()

    while True:
        data_chunk = data_file.read(chunk_size)
        if not data_chunk:
            break  # End of file reached, exit the loop

        # Send the binary data chunk to the server
        print(data_chunk)
        client_socket.sendto(data_chunk, (server_host, server_port))

    client_socket.sendto(b"END_OF_TRANSMISSION", (server_host, server_port))
    # Receive the final hash digest from the server
    response, server_address = client_socket.recvfrom(64)  # Adjust buffer size as needed

    # Record transfer time end
    transfer_end_time = time.time()

    # Print the received hash digest
    print(f"Received hash digest: {response.decode('utf-8')}")

    # Calculate and print times
    print(f"Transfer time: {transfer_end_time - transfer_start_time}")


