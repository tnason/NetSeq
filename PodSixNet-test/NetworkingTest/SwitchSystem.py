from ServerObj import ServerObj
from Client import Client

import sys
from sys import stdin
from time import sleep

def server_function():
    print "Starting a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")
    s = ServerObj(localaddr=(host, int(port)))

    i = 0
    while i < 3600:
        s.update()
        sleep(.1)
        i += 1

def client_function():
    print "Connecting to a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")
    c = Client(host, int(port))
    c.send_packet("hello!")
    sleep(.01)
    i = 0
    #wait to get packetConfirm
    while i < 3:
        c.Loop()
        sleep(.1)
        i += 1

while 1:
    print "MENU!"
    print "(1) Server"
    print "(2) Client"  
    sys.stdout.write("Which choice would you like? " )
    choice = stdin.readline().rstrip("\n")
    print ""
    if int(choice) == 1:
       server_function()
       break
    elif int(choice) == 2:
       client_function()
    else:
       print "Please enter either '1' or '2'!"
       print ""
       print ""



