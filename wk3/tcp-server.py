import socket
import threading

HOST='127.0.0.1'
PORT=9999

def handle_client(client):
  with client:
    while True:
      if client == None:
        break
      data = client.recv(1024)
      # begin protocol processing
      processed_data = data.upper()
      # end protocol
      client.sendall(processed_data)
    

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