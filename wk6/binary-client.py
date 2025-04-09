import socket
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

def get_request(command):
  c = command.strip()
  items = c.split(' ')
  request = Request(items[0], items[1], ' '.join(items[2:]))
  stream = io.BytesIO()
  pickle.dump(request, stream)
  serialized_payload = stream.getvalue()
  # add header size to length
  payload_length = len(serialized_payload) + 1
  return payload_length.to_bytes(1, byteorder='big') + serialized_payload

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
  client_socket.connect((HOST, PORT))
  command = ''
  while command.strip() != 'exit':
    command = input('connected>')
    # request is a byte array
    request = get_request(command)
    client_socket.send(request)
    data = client_socket.recv(BUFFER_SIZE)
    if not data:
      break
    binary_data = data
    full_data = binary_data
    message_length = binary_data[0]
    remaining = message_length - BUFFER_SIZE
    while remaining > 0:
      data = client_socket.recv(BUFFER_SIZE)
      binary_data = data
      full_data = full_data + binary_data
      remaining -= len(binary_data)
    stream = io.BytesIO(full_data[1:])
    response = pickle.load(stream)
    print(response.payload)