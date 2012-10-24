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
from server_obj import Server_Obj

class NetworkHandler():

    NOT_CONNECTED = 0
    NETWORK_CLIENT = 1
    NETWORK_SERVER = 2

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
        self.connected = NETWORK_CLIENT
        self.client = Client(host, int(port))
        #TODO: setup client, client_thread

    def start_server(self, server_ip, server_port):
        """server_ip sent as a string, server_port as an int"""
        self.connected = NETWORK_SERVER
        #TODO: setup server, server_thread, then client, client_thread

    def terminate_connections(self):
        if(self.connected == NOT_CONNECTED)
            #TODO: error message?
        elif(self.connected == NETWORK_CLIENT)
            client_thread.terminate()
            client_thread = None
        elif(self.connected == NETWORK_SERVER)
            server_thread.terminate()
            client_thread.terminate()
            server_thread = None
            client_thread = None

        self.connected = NOT_CONNECTED
            
    def send_note(self, Note):
        if(self.connected != NOT_CONNECTED)
            client_thread.
