import socket

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
  client_socket.sendto(b'Hello world!', (HOST, PORT))
  message = client_socket.recvfrom(1024)
  print(message)