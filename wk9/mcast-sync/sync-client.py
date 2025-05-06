import socket
import struct

MCAST_GROUP = '224.0.0.1'
MCAST_PORT = 12345

FILE_SERVER = '127.0.0.1'
FILE_PORT = 9999

DEST_DIRECTORY = './temp-receive'

def main():
  server_address = ('', MCAST_PORT)
  notification_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  notification_socket.bind(server_address)

  group = socket.inet_aton(MCAST_GROUP)
  multicast_request =  struct.pack('4sL', group, socket.INADDR_ANY)
  notification_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)

  while True:
    data, address = notification_socket.recvfrom(1024)
    filename = data.decode(encoding='utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
      file_socket.connect((FILE_SERVER, FILE_PORT))
      file_socket.sendall(filename.encode('utf-8'))
      data = file_socket.recv(1024)
      with open(f'{DEST_DIRECTORY}/{filename}', 'wb') as f:
        f.write(data)

if __name__ == '__main__':
  main()