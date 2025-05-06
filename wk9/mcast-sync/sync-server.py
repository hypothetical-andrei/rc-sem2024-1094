import socketserver
import inotify.adapters
import threading
import socket

SOURCE_DIRECTORY='./temp'

def file_watch(directory):
  notifier = inotify.adapters.Inotify()
  notifier.add_watch(directory)
  for event in notifier.event_gen(yield_nones=False):
    (_, type_names, path, filenames) = event
    if len(filenames) == 1 and len(type_names) == 1 and type_names[0] == 'IN_CLOSE_WRITE':
      send_multicast(filenames[0])

def send_multicast(filename):
  MCAST_GROUP = '224.0.0.1'
  MCAST_PORT = 12345
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
  sock.sendto(filename.encode('utf-8'), (MCAST_GROUP, MCAST_PORT))

class SyncTcpHandler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    filename = self.data.decode()
    print(f'sending file {filename}')
    with open(f'{SOURCE_DIRECTORY}/{filename}', 'rb') as f:
      self.request.sendall(f.read())

def main():
  HOST, PORT = 'localhost', 9999
  watch_thread = threading.Thread(target=file_watch, args=(SOURCE_DIRECTORY, ))
  watch_thread.start()
  with socketserver.TCPServer((HOST, PORT), SyncTcpHandler) as file_server:
    file_server.serve_forever()

if __name__ == '__main__':
  main()