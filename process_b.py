import socket
import hashlib

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IP and port for Process B
server_address = ('process_b_host', 12345)

# Bind the socket to the server address
sock.bind(server_address)

# Receive the message from Process A
data, address = sock.recvfrom(1024)

# Calculate the SHA-256 hash digest
message = data.decode()
hash_digest = hashlib.sha256(message.encode()).hexdigest()

print(f"Received message: {message}")
print(f"SHA-256 hash digest: {hash_digest}")

# Close the socket
sock.close()
