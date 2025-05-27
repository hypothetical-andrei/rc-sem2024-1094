import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3333  # Port to listen on (non-privileged ports are > 1023)

is_running = True

def handle_client(client, data):
  try:
    client.sendall(data)
    client.close()
  except IOError as e:
    print(e)

def accept(server, data):
  while is_running:
    client, addr = server.accept()
    print(f"{addr} has connected")
    client_thread = threading.Thread(target=handle_client, args=(client, data, ))
    client_thread.start()

def main():
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open('resource.jpg', 'rb') as f:
      data = f.read()
    print('total: ', len(data))
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept, args=(server, data, ))
    accept_thread.start()
    accept_thread.join()
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()

if __name__ == '__main__':
  main()