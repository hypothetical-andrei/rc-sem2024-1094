import socketserver

class MyTcpHandler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    self.request.sendall(self.data.upper())

if __name__ == '__main__':
  HOST = '127.0.0.1'
  PORT = 9999
  with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      server.shutdown()