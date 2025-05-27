#biclient seed
import socket
import threading
import struct

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server
# LOCAL_PORT = 3334
LOCAL_STORAGE = './client-storage'
BUFFER_SIZE = 1024

def active_get(command_socket, command):
	_, filename = command.strip().split(' ')
	with open(f'{LOCAL_STORAGE}/{filename}', 'wb') as f:
		temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		temp_server.bind(('', 0))
		temp_server.listen()
		local_port = temp_server.getsockname()[1]
		command_socket.sendall(f'{command} {local_port}'.encode())
		data = command_socket.recv(1024)
		if data:
			print(data.decode('utf-8'))
		client, _ = temp_server.accept()
		data = client.recv(BUFFER_SIZE)
		full_data = data[1:]
		message_length = data[0]
		remaining = message_length - BUFFER_SIZE
		while remaining > 0:
			data = client.recv(BUFFER_SIZE)
			full_data = full_data + data
			remaining = remaining - len(data)
		f.write(full_data)
	temp_server.close()

def active_put(command_socket, command):
	_, filename = command.strip().split(' ')
	with open(f'{LOCAL_STORAGE}/{filename}', 'rb') as f:
		content = f.read()
		content_size = len(content)
		temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		temp_server.bind(('', 0))
		temp_server.listen()
		local_port = temp_server.getsockname()[1]
		command_socket.sendall(f'{command} {local_port}'.encode())
		client, _ = temp_server.accept()
		data = content_size.to_bytes(1, byteorder='big') + content
		client.sendall(data)
		temp_server.close()

def passive_get(command_socket, command):
		_, filename = command.strip().split(' ')
		with open(f'{LOCAL_STORAGE}/{filename}', 'wb') as f:
			command_socket.send(command.strip().encode('utf-8'))
			data = command_socket.recv(1024)
			host = command_socket.getpeername()[0]
			print(f'received port {data}')
			port = int(data.strip())
			print(f'HOST/PORT -> {host}/{port}')
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
				file_socket.connect((host, port))
				print('CONNECTED')
				data = file_socket.recv(BUFFER_SIZE)
				full_data = data[1:]
				message_length = data[0]
				remaining = message_length - BUFFER_SIZE
				while remaining > 0:
					data = client.recv(BUFFER_SIZE)
					full_data = full_data + data
					remaining = remaining - len(binary_data)
			f.write(full_data)

def passive_put(command_socket, command):
		_, filename = command.strip().split(' ')
		with open(f'{LOCAL_STORAGE}/{filename}', 'rb') as f:
			content = f.read()
			content_size = len(content)
			command_socket.send(command.strip().encode('utf-8'))
			data = command_socket.recv(1024)
			host = command_socket.getpeername()[0]
			port = int(data.strip())
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as file_socket:
				# print(f'HOST/PORT -> {host}/{port}')
				file_socket.connect((HOST, port))
				file_socket.sendall(content_size.to_bytes(1, byteorder='big') + content)

def process_command(command_socket, command):
	command_items = command.strip().split(' ')
	if command_items[0] == 'active_get':
		temp_server_thread = threading.Thread(target=active_get, args=(command_socket, command))
		temp_server_thread.start()
		temp_server_thread.join()
	elif command_items[0] == 'active_put':
		temp_server_thread = threading.Thread(target=active_put, args=(command_socket, command))
		temp_server_thread.start()
		temp_server_thread.join()
	elif command_items[0] == 'passive_put':
		temp_client_thread = threading.Thread(target=passive_put, args=(command_socket, command))
		temp_client_thread.start()
		temp_client_thread.join()
	elif command_items[0] == 'passive_get':
		temp_client_thread = threading.Thread(target=passive_get, args=(command_socket, command))
		temp_client_thread.start()
		temp_client_thread.join()	

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as command_socket:
		command_socket.connect((HOST, PORT))
		while True:
			command = input('->')
			process_command(command_socket, command)

if __name__ == '__main__':
		main()