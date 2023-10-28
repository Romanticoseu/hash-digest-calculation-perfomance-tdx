import socket
import os
import time
import logging
import subprocess
import yaml

# Define the server address (host and port)
server_host = os.getenv("SERVER_HOST_NAME") 
# server_host = '127.0.0.1'  # Change this to the server's IP
server_port = 12345

# Specify the path to the file containing data
data_file_dir = os.getenv("DATA_PATH")

chunk_size = 1024  # You can adjust this value as needed
delay_time = 0.01  # Adjust this value to control the send rate

def send_data(data_file_path, server_host, server_port, chunk_size, delay_time, size_flag):
    
    # Configure logging to write to a log file
    log_filename = "log/client_" + size_flag + '.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s')
    
    
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Record transfer time start
    transfer_start_time = time.time()

    i = 0
    with open(data_file_path, 'rb') as data_file:
        while True:
            data_chunk = data_file.read(chunk_size)
            if not data_chunk:
                break  # End of file reached, exit the loop

            client_socket.sendto(data_chunk, (server_host, server_port))
            i += 1

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
        total_delay_time = (i - 1) * delay_time
        logging.info(f"Transfer time: {transfer_end_time - transfer_start_time - total_delay_time}")

def generate_data(size_flag):
    generate_command = f"./generate.sh -s {size_flag}"
    subprocess.run(generate_command, shell=True)

def main():
    # Load configuration from config.yaml
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    client_config = config.get("client_config")

    if client_config:
        type = client_config.get("type")
        size = client_config.get("size")
        times = client_config.get("times")

        if type == "continuous":
            # Generate data for each size in the range
            size_range = size.split("-")
            start_size = int(size_range[0].strip())
            end_size = int(size_range[1].strip())
            for size_kb in range(start_size, end_size + 1):
                size_flag = f"{size_kb}kb"
                generate_data(size_flag)
                send_data(data_file_dir + f"/{size_flag}.txt", server_host, server_port, chunk_size, delay_time, size_flag)
        elif type == "discrete":
            # Generate data for each size in the list and repeat 'times' times
            size_list = size
            for size_flag in size_list:
                generate_data(size_flag)
                for _ in range(times):
                    send_data(data_file_dir + f"/{size_flag}.txt", server_host, server_port, chunk_size, delay_time, size_flag)
        else:
            print("Invalid 'type' in configuration. Use 'continuous' or 'discrete'.")

if __name__ == "__main__":
    main()
