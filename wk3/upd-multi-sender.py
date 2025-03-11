import socket

MCAST_GROUP = '224.0.0.1'
MCAST_PORT = 9999

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

sender_socket.sendto(b'Hello multicast!', (MCAST_GROUP, MCAST_PORT))