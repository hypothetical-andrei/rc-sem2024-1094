import socket
import threading

HOST = '127.0.0.1'
PORT = 9999
SECRET = 'supersecret'
is_running = True

class TopicList:
	def __init__(self):
		self.clients = []
		self.topics = {}
		self.lock = threading.Lock()
	def add_client(self, client):
		with self.lock:
			self.clients.append(client)
	def remove_client(self, client):
		with self.lock:
			self.clients.remove(client)
			for topic, clients in self.topics:
				clients.remove(client)
	def subscribe(self, topic, client):
		with self.lock:
			self.topics.setdefault(topic, [])
			self.topics[topic].append(client)
	def unsubscribe(self, topic, client):
		with self.lock:
			self.topics[topic].remove(client)

global_state = TopicList()

class Request:
	def __init__(self, command, params):
		self.type = command
		self.params = params

class Response:
	def __init__(self, status, payload):
		self.status = status
		self.payload = payload

def serialize(response):
	return bytes(str(response.status) + ' ' + response.payload, encoding = 'utf-8')

def deserialize(request):
	items = request.decode('utf-8').strip().split(' ')
	if len(items) > 1:
		return Request(items[0], items[1:])
	return Request(items[0], None)

class StateMachine:
	def __init__(self, client, global_state):
		self.transitions = {}
		self.start_state = None
		self.end_states = []
		self.current_state = None
		self.global_state = global_state
		self.client = client
	def set_start(self, start):
		self.start_state = start
		self.current_state = start
	def add_transition(self, state_name, command, transition, end_state = False):
		self.transitions.setdefault(state_name, {})
		self.transitions[state_name][command] = transition
		if end_state:
			self.end_states.append(end_state)
	def process_command(self, unpacked_request):
		if unpacked_request.type in self.transitions[self.current_state]:
			handler = self.transitions[self.current_state][unpacked_request.type]
			if not handler:
				return Response(-4, 'cannot transition from this state')
			else:
				(new_state, response) = handler(unpacked_request, self.global_state, self.client)
				self.current_state = new_state
				return response
		else:
			return Response(-4, 'cannot transition from this state')

def request_connect(request, global_state, client):
	if request.params and len(request.params) > 0:
		if request.params[0] == SECRET:
			return ('auth', Response(0, 'you are in'))
		else:
			return ('start', Response(-2, 'you do not know the secret'))
	else:
		return ('start', Response(-1, 'not enough params'))

def request_disconnect(request, global_state, client):
	return ('start', Response(0, 'you are now out'))

def request_subscribe(request, global_state, client):
	if request.params and len(request.params) > 0:
		global_state.subscribe(request.params[0], client)
		return ('auth', Response(0, f'you are now subscribed to {request.params[0]}'))
	else:
		return ('auth', Response(-1, 'not enough params'))

def request_unsubscribe(request, global_state, client):
	if request.params and len(request.params) > 0:
		global_state.unsubscribe(request.params[0], client)
		return ('auth', Response(0, f'you are now unsubscribed from {request.params[0]}'))
	else:
		return ('auth', Response(-1, 'not enough params'))

def request_publish(request, global_state, client):
	if request.params and len(request.params) > 1:
		topic = request.params[0]
		data = ' '.join(request.params[1:])
		if topic in global_state.topics:
			for c in global_state.topics[topic]:
				if c != client:
					handle_client_write(c, Response(2, data))
					return ('auth', Response(0, 'message was published'))
		else:
			return ('auth', Response(-2, 'topic does not exist'))
	else:
		return ('auth', Response(-1, 'not enough params'))

class TopicProtocol(StateMachine):
	def __init__(self, client, global_state):
		super().__init__(client, global_state)
		self.set_start('start')
		self.add_transition('start', 'connect', request_connect)
		self.add_transition('auth', 'disconnect', request_disconnect)
		self.add_transition('auth', 'subscribe', request_subscribe)
		self.add_transition('auth', 'unsubscribe', request_unsubscribe)
		self.add_transition('auth', 'publish', request_publish)

def handle_client_write(client, response):
	client.sendall(serialize(response))

def handle_client_read(client):
	protocol = TopicProtocol(client, global_state)
	while True:
		if client == None:
			break
		data = client.recv(1024)
		if not data:
			break
		unpacked_request = deserialize(data)
		response = protocol.process_command(unpacked_request)
		handle_client_write(client, response)

def accept_clients(server):
	while is_running:
		client, address = server.accept()
		global_state.add_client(client)
		print(f'{address} has connected')
		client_read_thread = threading.Thread(target=handle_client_read, args=(client, ))
		client_read_thread.start()

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		server.bind((HOST, PORT))
		server.listen()
		accept_thread = threading.Thread(target=accept_clients, args=(server, ))
		accept_thread.start()
		accept_thread.join()
	finally:
		if server:
			server.close()

if __name__ == '__main__':
	main()
