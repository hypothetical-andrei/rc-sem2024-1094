import io
import pickle

def serialize(message):
	stream = io.BytesIO()
	pickle.dump(message, stream)
	serialized_message = stream.getvalue()
	return serialized_message

def deserialize(message):
	stream = io.BytesIO(message)
	deserialized_message = pickle.load(stream)
	return deserialized_message
