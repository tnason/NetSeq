import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

#do i need to thread like they did?
#Yeah, the stdin call is blocking, so I do.
#TODO: Change this from the loop structure to polling for key press events
from thread import *

class Client(ConnectionListener):
    def __init__(self, host, port):
            self.Connect((host, port))
            print "Chat client started"
            #"Bad" threaded input loop
            t = start_new_thread(self.InputLoop, ())

    def Loop(self):
            connection.Pump()
            self.Pump()

    def InputLoop(self):
            while 1:
                connection.Send({"action": "packet", "message": stdin.readline().rstrip("\n")})

    #Network events
    def Network_packetConfirm(self, data):
        print "Packet confirmation received." + str(data['packet'])

    def Network_chatSend(self, data):
        print str(data['text']);

    #built in Network events
    def Network_connected(self, data):
    	print "You are now connected to the server"
	
    def Network_error(self, data):
	print 'error:', data['error'][1]
	connection.Close()
	
    def Network_disconnected(self, data):
	print 'Server disconnected'
	exit()

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	while 1:
		c.Loop()
		sleep(0.001)
