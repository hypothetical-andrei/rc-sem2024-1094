import socket
import threading

HOST='127.0.0.1'
PORT=9999

class ClientList:
  def __init__(self):
    self.clients = []
    self.lock = threading.Lock()
  def add_client(self, client):
    with self.lock:
      self.clients.append(client)
  def remove_client(self, client):
    with self.lock:
      self.clients.remove(client)

clients = ClientList()


def handle_client_write(client, data):
  for c in clients.clients:
    if c != client:
      c.sendall(data)

def handle_client_read(client, callback = handle_client_write):
  try:
    while True:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      callback(client, data)
  except OSError:
    clients.remove(client)  

def accept_clients(server):
  while True:
    client, addr = server.accept()
    print(f'{addr} has connected')
    client_read_thread = threading.Thread(target=handle_client_read, args=(client, handle_client_write, ))
    client_read_thread.start()

def main():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
    accept_thread.start()
    accept_thread.join()
  except KeyboardInterrupt:
    if server_socket:
      server_socket.close()

if __name__ == '__main__':
  main()
