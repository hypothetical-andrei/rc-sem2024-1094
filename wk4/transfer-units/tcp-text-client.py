import socket

HOST='127.0.0.1'
PORT=9999
BUFFER_SIZE=4

def get_network_message(message):
  command = message.strip()
  content_length = len(command)
  total_length = content_length + len(str(content_length)) + 1
  return f'{total_length} {command}'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
  client_socket.connect((HOST, PORT))
  while True:
    print('give me some data to send')
    message = input('->')
    client_socket.sendall(bytes(get_network_message(message), encoding='utf-8'))
    data = client_socket.recv(BUFFER_SIZE)
    if not data:
      break
    string_data = data.decode('utf-8')
    full_data = string_data
    message_length = int(string_data.split(' ')[0])
    remaining = message_length - len(string_data)
    while remaining > 0:
      data = client_socket.recv(BUFFER_SIZE)
      string_data = data.decode('utf-8')
      full_data += string_data
      remaining -= len(string_data)
    print(f'Received from server {full_data}')
