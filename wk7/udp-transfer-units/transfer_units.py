from enum import Enum

class RequestMessageType(Enum):
	CONNECT = 1
	SEND = 2
	LIST = 3
	DISCONNECT = 4

class ResponseMessageType(Enum):
	OK = 1
	ERR_CONNECTED = 2

class RequestMessage():
	def __init__(self, message_type, payload = ''):
		self.message_type = message_type
		self.payload = payload
	def	__str__(self):
		return f'''
------REQUEST-----
TYPE: {self.message_type}
{self.payload}
------------------
		'''


class ResponseMessage():
	def __init__(self, message_type, payload = ''):
		self.message_type = message_type
		self.payload = payload
	def	__str__(self):
		return f'''
-----RESPONSE-----
TYPE: {self.message_type}
{self.payload}
------------------
		'''
