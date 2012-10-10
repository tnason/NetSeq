#client module file

import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

from thread import *

class Client(ConnectionListener):
    def __init__(self, host, port):
            self.Connect((host, port))
            print "Chat client started"
            #"Bad" threaded input loop
            #t = start_new_thread(self.InputLoop, ())

    def Loop(self):
            connection.Pump()
            self.Pump()

    def send_packet(self, data):
            connection.Send({"action": "packet", "message": str(data)})

#    def InputLoop(self):
#            while 1:
#                connection.Send({"action": "packet", "message": stdin.readline().rstrip("\n")})

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

