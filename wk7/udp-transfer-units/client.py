import socket

from transfer_units import RequestMessageType, ResponseMessageType, RequestMessage, ResponseMessage
from serialization import serialize, deserialize

def main():
	HOST = '127.0.0.1'
	PORT = 9999
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
		while True:
			data = input('note-storage>')
			items = data.strip().split(' ')
			command = items[0]
			if command == 'connect':
				client_socket.sendto(serialize(RequestMessage(RequestMessageType.CONNECT)), (HOST, PORT))
			elif command == 'send':
				client_socket.sendto(serialize(RequestMessage(RequestMessageType.SEND, items[1])), (HOST, PORT))
			elif command == 'list':
				client_socket.sendto(serialize(RequestMessage(RequestMessageType.LIST)), (HOST, PORT))
			elif command == 'disconnect':
				client_socket.sendto(serialize(RequestMessage(RequestMessageType.DISCONNECT)), (HOST, PORT))
			else:
				print('unknown command, please retry!')
				continue
			message, _ = client_socket.recvfrom(1024)
			deserialized_response = deserialize(message)
			print(deserialized_response)

if __name__ == '__main__':
	main()
