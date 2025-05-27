import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server

with open('out.jpg', 'wb') as f:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      part = s.recv(1024)
      count = len(part)
      bytes_received = len(part)

      while bytes_received > 0:
        count += bytes_received
        f.write(part)
        print(f'read {count}')
        if bytes_received > 0:
          part = s.recv(1024)
          bytes_received = len(part)
        else:
          break
