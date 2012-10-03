from ServerObj import ServerObj
from Client import Client

import sys
from sys import stdin
from time import sleep

print "Server?: "
host = stdin.readline().rstrip("\n")
print "Port?: "
port = stdin.readline().rstrip("\n")
s = ServerObj(host, int(port));

sleep(10)


c = Client(host, int(port));
c.connection.Send({"action": "packet", "message": "hello!"});
c.connection.Pump()
c.Pump()
