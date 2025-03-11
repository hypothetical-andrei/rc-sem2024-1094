import socket
import struct

MCAST_GROUP = '224.0.0.1'
MCAST_PORT = 9999

server_address = (MCAST_GROUP, MCAST_PORT)

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiver_socket.bind(server_address)

group = socket.inet_aton(MCAST_GROUP)
multicast_request =  struct.pack('4sL', group, socket.INADDR_ANY)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)

while True:
  data, address = receiver_socket.recvfrom(1024)
  print(f'received {data} from {address}')

