import socket

HOST='127.0.0.1'
PORT=9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
  client_socket.connect((HOST, PORT))
  while True:
    print('give me some data to send')
    message = input()
    client_socket.sendall(bytes(message, encoding='utf-8'))
    data = client_socket.recv(1024)
    print(f'Received from server {data}')