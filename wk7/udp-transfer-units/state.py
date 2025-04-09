class State:
	def __init__(self):
		self.connections = {}
	def add_connection(self, address):
		self.connections.setdefault(address, [])
	def remove_connection(self, address):
		del self.connections[address]
	def add_note(self, address, note):
		self.connections[address].append(note)
	def get_notes(self, address):
		return '\n'.join(self.connections[address])
