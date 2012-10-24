# This will provide an interface to the network for the main app

""" Functions to start a server/client pair or a single client will be provided
        This function will handle the creation of those objects
            And the launching/killing of their network threads
    The main app will then be able to send network data without caring if it is
    a server or a client

    This class will also notify the main app upon network termination
        And allow for remote termination from the network app
"""
from client import Client
from server_obj import ServerObj
from network_thread import NetworkThread
from time import sleep

NOT_CONNECTED = 0
NETWORK_CLIENT = 1
NETWORK_SERVER = 2

class NetworkHandler():


    def __init__(self, music_player, gui):
        """constructor for the network handler"""
        self.music_player = music_player
        self.gui = gui

        self.server = None
        self.client = None
        self.server_thread = None
        self.client_thread = None
        self.connected = NOT_CONNECTED #integer flag indicating connection state
        

    def connect_to_server(self, server_ip, server_port):
        """server_ip sent as a string, server_port as an int"""
        self.client = Client(server_ip, server_port)
        #TODO: Check to make sure client was made successfully?
        self.client_thread = NetworkThread("client", self.client)
        self.client_thread.start()
        self.connected = NETWORK_CLIENT
        
    def start_server(self, server_ip, server_port):
        """server_ip sent as a string, server_port as an int"""
        self.server = ServerObj(localaddr=(server_ip, server_port))
        #TODO: Check to make sure server was made successfully?
        self.server_thread = NetworkThread("server", self.server)
        self.server_thread.start()

        self.client = Client(server_ip, server_port)
        #TODO: Check to make sure client was made successfully?
        self.client_thread = NetworkThread("client", self.client)
        self.client_thread.start()
        self.connected = NETWORK_SERVER
        
    def terminate_connections(self):
        if self.connected == NOT_CONNECTED:
            pass
            #TODO: error message?
        elif self.connected == NETWORK_CLIENT:
            client_thread.terminate()
            client_thread = None
        elif self.connected == NETWORK_SERVER:
            server_thread.terminate()
            client_thread.terminate()
            server_thread = None
            client_thread = None

        self.connected = NOT_CONNECTED
        #TODO: Anything else need to be done to clean up network objects?
            
    def send_note(self, note):
        """send note wrapper method"""
        if self.connected != NOT_CONNECTED:
            self.client.send_note(note)

    def send_volume(self, volume, track_id):
        """send volume wrapper method"""
        if self.connected != NOT_CONNECTED:
            self.client.send_volume(volume, track_id)

    def send_tempo(self, tempo):
        """send tempo wrapper method"""
        if self.connected != NOT_CONNECTED:
            self.client.send_tempo(tempo)

    def send_reverb(self, reverb, track_id):
        """send reverb wrapper method"""
        if self.connected != NOT_CONNECTED:
            self.client.send_reverb(reverb, track_id)

    def send_session(self, session):
        """send session wrapper method"""
        if self.connected != NOT_CONNECTED:
            self.client.send_session(session)

#network testing code
if __name__ == "__main__":
    test = NetworkHandler(None, None)
    test.start_server("localhost", int(25000))
    sleep(.1)
    test.send_volume(1, 2)
    
            
