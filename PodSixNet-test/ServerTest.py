#Server example for sending data over the network
import sys
from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

#Server representation of a connected client
class ClientChannel(Channel):
        def __init__(self, *args, **kwargs):
            Channel.__init__(self, *args, **kwargs)

        def Close(self):
            self._server.DelClient(self)

        # Network functions

        def Network_packet(self, data):
            self.Send({"action": "packetConfirm", "packet": 123})
            for c in self._server.clients:
                if c != self:
                    c.Send({"action": "chatSend", "text": data['message']})
            

class ServerTest(Server):
        channelClass = ClientChannel

        def __init__(self, *args, **kwargs):
            Server.__init__(self, *args, **kwargs)
            self.clients = WeakKeyDictionary() #Store weak references to clients
            print 'Server launched'

        def Connected(self, channel, addr):
            self.AddClient(channel)

        def AddClient(self, client):
            print "New client at " + str(client.addr)
            self.clients[client] = True
            print "clients", [c for c in self.clients]

        def DelClient(self, client):
            print "Deleting " + str(client.addr)
            del self.clients[client]

        def Broadcast(self, data):
            [c.Send(data) for c in self.clients]

        def Run(self):
            while True:
                    self.Pump()
                    sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	s = ServerTest(localaddr=(host, int(port)))
	s.Run()


