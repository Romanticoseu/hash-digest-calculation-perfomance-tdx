import socket

# Define the message
message = "Hello, Process B!"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IP and port for Process B
server_address = ('process_b_host', 12345)

# Send the message
sock.sendto(message.encode(), server_address)

# Close the socket
sock.close()
