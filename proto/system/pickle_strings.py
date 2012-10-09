import pickle

data = ["dennis", 5, "Hello!", 122223]
pickled_string = pickle.dumps(data)

print "Data: ", data
print "Pickled: ", pickled_string

unpickled_string = pickle.loads(pickled_string)

print "Unpickled: ", unpickled_string
