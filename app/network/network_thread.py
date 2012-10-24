import threading
import time
from client import Client
from server_obj import ServerObj

class NetworkThread(threading.Thread):
    def __init__(self, name, network_object):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.network_object = network_object
        self._stopevent = threading.Event()


    def run(self):
        print "thread run loop starting"
        while not self._stopevent.isSet():
            self.network_object.Loop()
            self._stopevent.wait(0.001)

        print "thread terminate event received"

    def terminate(self):
        """for external signal to terminate thread"""
        print "thread exiting"
        self._stopevent.set()
        threading.Thread.join(self, timeout=None)
        
