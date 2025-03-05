import socket

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
  server_socket.bind((HOST, PORT))
  while True:
    message, address = server_socket.recvfrom(1024)
    server_socket.sendto(message.upper(), address)