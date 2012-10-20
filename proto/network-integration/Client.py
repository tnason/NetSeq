#client module file

import sys
from time import sleep
from sys import stdin, exit

from pyo import *

import random

from PodSixNet.Connection import connection, ConnectionListener

from thread import *

class Client(ConnectionListener):

    pyo_server = None
    wav = None
    frequency = -1
    
    def __init__(self, host, port):
            self.Connect((host, port))
            print "Chat client started"
            #"Bad" threaded input loop
            #t = start_new_thread(self.InputLoop, ())

    def initialize_pyo(self):
        global pyo_server
        global wav
        pyo_server = Server().boot()
        pyo_server.start()
        wav = SquareTable()

    def run_loop(self):
        self.initialize_pyo()
        self.set_frequency()
        while True:
                self.Loop()
                sleep(.01)

    def Loop(self):
            connection.Pump()
            self.Pump()

    def send_packet(self, data):
            connection.Send({"action": "packet", "message": str(data)})

    def send_frequency(self):
            #self.play_frequency(frequency)
            connection.Send({"action": "send_frequency", "frequency": str(frequency)})

    def play_frequency(self, freq):
            a = Osc(table=wav, freq=freq, mul=1).out()
            time.sleep(2)
            a.stop()

    def set_frequency(self):
            global frequency
            random.seed()
            frequency = random.randrange(150, 5000)
            print frequency

#    def InputLoop(self):
#            while 1:
#                connection.Send({"action": "packet", "message": stdin.readline().rstrip("\n")})

    #Network events
    def Network_play_frequency(self, data):
        print "===received network prompt to play sound==="
	self.play_frequency(int(data['frequency']))

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

