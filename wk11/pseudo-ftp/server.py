# biserver seed
import socket
import threading
import os
import struct
import io

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3333  # Port to listen on (non-privileged ports are > 1023)

FILE_ROOT = './server-storage'
BUFFER_SIZE = 1024
is_running = True

def process_command(client, request):
	command_items = request.decode('utf-8').strip().split(' ')
	command_mappings = {
		'list': process_list,
		'active_get': active_get,
		'active_put': active_put,
		'passive_get': passive_get,
		'passive_put': passive_put
	}
	if len(command_items) > 0:
		if command_items[0] in command_mappings:
			response = command_mappings[command_items[0]](client, command_items)
		else:
			print(command_items)

def process_list(client, command_items):
	files = os.listdir(FILE_ROOT)
	return '\n'.join(files)

def active_get(client, command_items):
	if len(command_items) < 3:
		client.sendall(b'not enough params')
	else:
		_, filename, port = command_items
		with open(f'{FILE_ROOT}/{filename}', 'rb') as f:
			content = f.read()
			content_size = len(content)
			host = client.getpeername()[0]
			port = int(port)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
				print(f'transfer to HOST/PORT -> {host}/{port}')
				file_socket.connect((host, port))
				file_socket.sendall(content_size.to_bytes(1, byteorder='big') + content)
		client.sendall(b'done!')

def active_put(client, command_items):
	if len(command_items) < 3:
		client.sendall(b'not enough params')
	else:
		_, filename, port = command_items
		with open(f'{FILE_ROOT}/{filename}', 'wb') as f:
			host = client.getpeername()[0]
			port = int(port)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
				file_socket.connect((host, port))
				data = file_socket.recv(BUFFER_SIZE)
				print(f'data {data}')
				full_data = data[1:]
				message_length = data[0]
				print('l', message_length)
				remaining = message_length - BUFFER_SIZE
				while remaining > 0:
					data = file_socket.recv(BUFFER_SIZE)
					full_data = full_data + data
					remaining = remaining - len(data)
				f.write(full_data)
		client.sendall(b'done!')

def passive_put(client, command_items):
	_, filename = command_items
	with open(f'{FILE_ROOT}/{filename}', 'wb') as f:
		temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		temp_server.bind(('', 0))
		temp_server.listen()
		local_port = temp_server.getsockname()[1]
		client.sendall(f'{local_port}'.encode('utf-8'))
		temp_client, _ = temp_server.accept()
		full_data = bytes()
		data = temp_client.recv(BUFFER_SIZE)
		binary_data = data
		full_data = binary_data[1:]
		message_length = binary_data[0]
		remaining = message_length - BUFFER_SIZE
		while remaining > 0:
				data = temp_client.recv(BUFFER_SIZE)
				binary_data = data
				full_data = full_data + binary_data
				remaining = remaining - len(binary_data)
		# print(f'finished receiving {filename}')
		f.write(full_data)
	temp_server.close()

def passive_get(client, command_items):
	_, filename = command_items
	with open(f'{FILE_ROOT}/{filename}', 'rb') as f:
		content = f.read()
		content_size = len(content)
		temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		temp_server.bind(('', 0))
		temp_server.listen()
		local_port = temp_server.getsockname()[1]
		print(f'inside open file {local_port}')
		client.sendall(f'{local_port}'.encode('utf-8'))
		temp_client, _ = temp_server.accept()
		temp_client.sendall(content_size.to_bytes(1, byteorder='big') + content)
		temp_server.close()

def handle_client_commands(client):
	with client:
		while True:
			if client == None:
				break
			request = client.recv(1024)
			if request:
				process_command(client, request)

def accept(server):
	while is_running:
		client, addr = server.accept()
		print(f"{addr} has connected")
		command_thread = threading.Thread(target=handle_client_commands, args=(client, ))
		command_thread.start()

def main():
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((HOST, PORT))
		server.listen()
		accept_thread = threading.Thread(target=accept, args=(server,))
		accept_thread.start()
		accept_thread.join()
	except BaseException as err:
		print(err)
	finally:
		if server:
			server.close()

if __name__ == '__main__':
	main()