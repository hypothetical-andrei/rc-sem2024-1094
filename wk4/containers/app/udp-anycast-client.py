import socket
# sudo ip -6 addr add 2001:db8::1/64 dev lo
ANYCAST_ADDR = "2001:db8:1::20"  # Simulated anycast address
PORT = 9999

def anycast_client():
    """Send a message to the anycast address."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    message = b"Hello, anycast server!"
    sock.sendto(message, (ANYCAST_ADDR, PORT))

    data, addr = sock.recvfrom(1024)
    print(f"Received response: '{data.decode()}' from {addr}")

if __name__ == "__main__":
    anycast_client()
