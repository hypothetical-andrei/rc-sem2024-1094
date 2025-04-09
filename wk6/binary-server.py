import socket
import threading
import io
import pickle

HOST='127.0.0.1'
PORT=9999
BUFFER_SIZE=4

class Response:
  def __init__(self, payload):
    self.payload = payload

class Request:
  def __init__(self, command, key, resource = None):
    self.command = command
    self.key = key
    self.resource = resource

class State:
  def __init__(self):
    self.resources = {}
    self.lock = threading.Lock()
  def add(self, key, resource):
    self.lock.acquire()
    # actually add key
    self.resources[key] = resource
    self.lock.release()
  def remove(self, key):
    if key in self.resources:
      self.lock.acquire()
      self.resources.pop(key)
      self.lock.release()
  def get(self, key):
    if key in self.resources:
      return self.resources[key]
    return None

state = State()

def process_command(full_data):
  payload = full_data[1:]
  stream = io.BytesIO(payload)
  request = pickle.load(stream)
  payload = 'command not recongnized, doing nothing'
  if request.command == 'add':
    state.add(request.key, request.resource)
    payload = f'{request.key} added'
  elif request.command == 'remove':
    state.remove(request.key)
    payload = f'{request.key} removed'
  elif request.command == 'get':
    payload = state.get(request.key)
    if not payload:
      payload = f'{request.key} does not exist'
  stream = io.BytesIO()
  pickle.dump(Response(payload), stream)
  serialized_payload = stream.getvalue()
  # add header size to length
  payload_length = len(serialized_payload) + 1 
  return payload_length.to_bytes(1, byteorder='big') + serialized_payload

def handle_client(client):
  with client:
    while True:
      if client == None:
        break
      is_new_command = True
      data = client.recv(BUFFER_SIZE)
      if not data:
        break
      binary_data = data
      full_data = binary_data
      message_length = binary_data[0]
      remaining = message_length - BUFFER_SIZE
      while remaining > 0:
        data = client.recv(BUFFER_SIZE)
        binary_data = data
        full_data = full_data + binary_data
        remaining -= len(binary_data)
      response = process_command(full_data)
      client.sendall(response)

def accept_clients(server):
  while True:
    client, addr = server.accept()
    print(f'{addr} has connected')
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

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
