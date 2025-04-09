import socket

from transfer_units import RequestMessageType, ResponseMessageType, RequestMessage, ResponseMessage
from state import State
from serialization import serialize, deserialize

def main():
	PORT = 9999

	state = State()

	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
		server_socket.bind(('', PORT))
		while True:
			message, address = server_socket.recvfrom(1024)
			request = deserialize(message)
			print(request)
			if request.message_type == RequestMessageType.CONNECT:
				state.add_connection(address)
				server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)
			if request.message_type == RequestMessageType.SEND:
				if address in state.connections:
					state.add_note(address, request.payload)
					server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)
				else:
					server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.ERR_CONNECTED)), address)
			if request.message_type == RequestMessageType.LIST:
				if address in state.connections:
					state.add_note(address, request.payload)
					server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK, state.get_notes(address))), address)
				else:
					server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.ERR_CONNECTED)), address)
			if request.message_type == RequestMessageType.DISCONNECT:
				state.remove_connection(address)
				server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)

if __name__ == '__main__':
	main()
