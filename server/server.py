import socket
import os
import hashlib
import time
import logging
import csv

tdx_flag = os.getenv("TDX_ENABLE")

# Configure logging to write to a log file
log_filename = 'server.log'
if tdx_flag:
    log_filename = 'tdx_' + log_filename
log_filename = './log/' + log_filename
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

# Define the path for the CSV file
csv_file_path = './log/res.csv'
tdx_enabled = 1 if tdx_flag == "true" else 0

# Define the server address (host and port)
server_host = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

# Increase the buffer size for receiving data
buffer_size = 1024

logging.info(f"Server listening on {server_host}:{server_port}")

while True:
    # Create an empty buffer to accumulate data
    data_buffer = b""  # Initialize as a byte string
    
    i = 0
    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(buffer_size)
        print(i, "\n", data)
        i+=1
        
        # Check index
        if data.startswith(b"INDEX"):
            index = data[len(b"INDEX"):].decode()
            csv_file_path = f'./log/res_{index}.csv'
        
        # Check if the message starts with SIZE_FLAG
        if data.startswith(b"SIZE_FLAG"):
            size_flag = data[len(b"SIZE_FLAG"):].decode()
            logging.warning(f"Received SIZE_FLAG: {size_flag}")
            
        if not data:
            logging.info("End of data received")
            break  # No more data received, exit the inner loop

        # Check for a special marker to exit the loop
        if data == b"END_OF_TRANSMISSION":
            logging.info("End of data received")
            break
        # Append the received data to the buffer
        data_buffer += data
        

    message = data_buffer.decode('utf-8')
    # Split the message into lines and count them
    lines = message.split('\n')
    line_count = len(lines)
    logging.info(f"Received from {client_address}: Lines: {line_count}")

    # Calculate the SHA-256 hash of the entire message
    hash_start_time = time.perf_counter()  # Record hash calculation start time
    sha256_hash = hashlib.sha256(message.encode()).hexdigest()
    hash_end_time = time.perf_counter()  # Record hash calculation end time
    logging.info(f"SHA-256 Hash: {sha256_hash}")

    # Send the hash and line count back to the client
    response_message = f"Hash: {sha256_hash}"
    server_socket.sendto(response_message.encode('utf-8'), client_address)

    # Calculate and log times
    logging.info(f"Hash calculation time: {hash_end_time - hash_start_time}")
    
    # Save the data to the CSV file
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['tdx_enabled', 'data_size', 'calculation_time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Check if the SIZE_FLAG is received
        if 'size_flag' in locals():
            writer.writerow({'tdx_enabled': tdx_enabled, 'data_size': size_flag, 'calculation_time': hash_end_time - hash_start_time})
