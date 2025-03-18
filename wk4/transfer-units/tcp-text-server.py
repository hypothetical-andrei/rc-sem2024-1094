import socket
import threading

HOST='127.0.0.1'
PORT=9999
BUFFER_SIZE=4

def process_command(full_data):
  items = full_data.split(' ')
  command = ' '.join(items[1:])
  print('command received', command)
  payload = 'Invalid command'
  if command == 'tic':
    payload = 'tac'
  elif command == 'tac':
    payload = 'tic'
  payload_length = len(payload)
  response = f'{payload_length + 1 + len(str(payload_length))} {payload}'
  return response

def handle_client(client):
  with client:
    while True:
      if client == None:
        break
      is_new_command = True
      data = client.recv(BUFFER_SIZE)
      if not data:
        break
      string_data = data.decode('utf-8')
      full_data = string_data
      # start of command looks like this: 7 et cqw
      message_length = int(string_data.split(' ')[0])
      remaining = message_length - len(string_data)
      while remaining > 0:
        data = client.recv(BUFFER_SIZE)
        string_data = data.decode('utf-8')
        full_data += string_data
        remaining -= len(string_data)
      print(full_data)
      response = process_command(full_data)
      print(response)
      client.sendall(response.encode('utf-8'))

def accept_clients(server):
  while True:
    client, addr = server.accept()
    print(f'{addr} has connected')
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

def main():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))
  server_socket.listen()
  accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
  accept_thread.start()
  accept_thread.join()

if __name__ == '__main__':
  main()
