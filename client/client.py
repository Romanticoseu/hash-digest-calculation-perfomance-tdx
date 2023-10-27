import socket
import os
import time
import logging
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description="Client script with -s size option")
# Add the -s option to specify the size
parser.add_argument("-s", "--size", help="Size option (e.g., 1kb, 10kb, 1mb, 10mb)")
# Parse the command-line arguments
args = parser.parse_args()
# Store the size option in the size_flag variable
size_flag = args.size

# Configure logging to write to a log file
log_filename = size_flag + '.log'
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

# Define the server address (host and port)
server_host = os.getenv("SERVER_HOST_NAME") 
# server_host = '127.0.0.1'  # Change this to the server's IP
server_port = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Specify the path to the file containing data
data_file_path = os.getenv("DATA_PATH")
# data_file_path = "./data/iris.data"

# Define the chunk size for reading and sending data
chunk_size = 1024  # You can adjust this value as needed
delay_time = 0.01  # Adjust this value to control the send rate

client_socket.sendto(b"SIZE_FLAG " + size_flag.encode(), (server_host, server_port))

# Open the data file for reading
with open(data_file_path + "/" + size_flag + ".txt", 'rb') as data_file:
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Record transfer time start
    transfer_start_time = time.time()
    
    i = 0
    while True:
        data_chunk = data_file.read(chunk_size)
        if not data_chunk:
            break  # End of file reached, exit the loop

        # Send the binary data chunk to the server
        print(i, "\n", data_chunk)
        i += 1
        client_socket.sendto(data_chunk, (server_host, server_port))
        
        # Introduce a delay to control the send rate
        time.sleep(delay_time)

    client_socket.sendto(b"END_OF_TRANSMISSION", (server_host, server_port))
    # Receive the final hash digest from the server
    response, server_address = client_socket.recvfrom(64)  # Adjust buffer size as needed

    # Record transfer time end
    transfer_end_time = time.time()

    # Print the received hash digest
    logging.info(f"Received hash digest: {response.decode('utf-8')}")

    # Calculate and log times
    total_delay_time = i * delay_time
    logging.info(f"Transfer time: {transfer_end_time - transfer_start_time - total_delay_time}")


