import socket

ANYCAST_ADDR = "::"  # Simulated anycast address
PORT = 9999

def anycast_server():
    """Simulated IPv6 anycast server."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((ANYCAST_ADDR, PORT))
    print(f"Anycast Server listening on [{ANYCAST_ADDR}]:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received '{data.decode()}' from {addr}")
        sock.sendto(b"Reply from anycast server", addr)

if __name__ == "__main__":
    anycast_server()
