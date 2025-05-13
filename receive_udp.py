import socket
import argparse
from protocol import MouseData

# Parse command-line arguments
parser = argparse.ArgumentParser(description='UDP Server')
parser.add_argument('--port', type=int, default=12345, help='Port number to bind to')
args = parser.parse_args()

HOST = 'localhost'
PORT = args.port

# Create UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, PORT))
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(4096)  # 4096 is a more standard buffer size
        print(f"Received from {addr}: {data}")

        Mouse_points = MouseData.Parse(data)
        print(f"Received {len(Mouse_points.points)} points: {Mouse_points.points}")