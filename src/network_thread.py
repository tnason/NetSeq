import threading
import time

class NetworkThread(threading.Thread):

    def __init__(self, name, network_object):
        """Create new network thread

        Arguments:
        name: descriptive name
        network_object: PodSixNet client or server to be threaded

        """

        threading.Thread.__init__(self, name=name)
        self.name = name
        self.network_object = network_object
        self._stopevent = threading.Event()

    def run(self):
        """Kick off network thread"""
    
        print "@@ thread run loop starting"
        while not self._stopevent.isSet():
            self.network_object.Loop()
            self._stopevent.wait(0.001)

    def terminate(self):
        """Terminate this network thread"""
        print "@@ thread exiting"
        self._stopevent.set()
        threading.Thread.join(self, timeout=None)
        self.network_object = None
        
