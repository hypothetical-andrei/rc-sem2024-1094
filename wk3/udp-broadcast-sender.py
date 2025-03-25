import socket

# # all the computers in the current network
BROADCAST_ADDRESS = '255.255.255.255'
BROADCAST_PORT = 9999

broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.sendto(b'Hello broadcast!', (BROADCAST_ADDRESS, BROADCAST_PORT))
