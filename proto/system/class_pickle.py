import pickle

class PickleMe:
    # We'll want to define our WAV files at this scope, if possible!! Don't
    # make them a property of self, which are the instance properties that will
    # be saved by 'pickle'
    hidden_attr = 3

    def __init__(self):
        another_hidden_attr = 900
        self.attr = 60

pickle_me = PickleMe()
pickle_string = pickle.dumps(pickle_me)
unpickle_me = pickle.loads(pickle_string)

print "PickleMe: ", pickle_me
print "Pickle String: ", pickle_string

print "Unpickled!"
print "unpickle_me.hidden_attr = ", unpickle_me.hidden_attr
