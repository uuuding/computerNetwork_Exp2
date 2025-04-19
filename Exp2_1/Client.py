import socket
import time

# Server settings
SERVER_HOST = '127.0.0.1'  # change to server IP if remote
SERVER_PORT = 12000
TIMEOUT = 1.0  # seconds
PING_COUNT = 10

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

# Statistics
rtts = []
lost_count = 0

print(f"Pinging {SERVER_HOST}:{SERVER_PORT} with {PING_COUNT} UDP packets:\n")

for seq in range(1, PING_COUNT + 1):
    # Prepare ping message
    send_time = time.time()
    message = f"PING {seq} {send_time}".encode()

    try:
        # Send ping
        client_socket.sendto(message, (SERVER_HOST, SERVER_PORT))

        # Wait for pong
        data, _ = client_socket.recvfrom(1024)
        recv_time = time.time()

        # Compute RTT
        rtt = recv_time - send_time
        rtts.append(rtt)

        # Decode and display
        print(f"Ping {seq}: Received '{data.decode()}' in {rtt:.4f} seconds")

    except socket.timeout:
        # Timeout
        lost_count += 1
        print(f"Ping {seq}: Request timed out.")

# Final statistics
print("\n--- Ping statistics ---")
print(f"Packets: Sent = {PING_COUNT}, Received = {PING_COUNT - lost_count}, Lost = {lost_count} ({lost_count / PING_COUNT * 100:.1f}% loss)")

if rtts:
    print(f"Approximate round trip times in milli-seconds:")
    print(f"    Minimum = {min(rtts) * 1000:.2f} ms, Maximum = {max(rtts) * 1000:.2f} ms, Average = {sum(rtts) / len(rtts) * 1000:.2f} ms")

# Close socket
client_socket.close()