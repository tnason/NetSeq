from ServerObj import ServerObj
from Client import Client

import sys
from sys import stdin
from time import sleep


sys.stdout.write("Server?: ")
host = stdin.readline().rstrip("\n")
sys.stdout.write("Port?: ")
port = stdin.readline().rstrip("\n")
s = ServerObj(localaddr=(host, int(port)));

sleep(1)


c = Client(host, int(port));
c.send_packet("hello!");
c.Loop()

s.update()
