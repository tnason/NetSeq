# This will provide an interface to the network for the main app

""" Functions to start a server/client pair or a single client will be provided
        This function will handle the creation of those objects
            And the launching/killing of their network threads
    The main app will then be able to send network data without caring if it is
    a server or a client

    This class will also notify the main app upon network termination
        And allow for remote termination from the network app
"""
from server_obj import ServerObj
from network_thread import NetworkThread
from music_player import MusicPlayer

from client import Client, ClientNetworkError

import sys
from time import sleep
import socket

NOT_CONNECTED = 0
NETWORK_CLIENT = 1
NETWORK_SERVER = 2

class NetworkHandler():
    """Primary interface to handle network interaction"""

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
        """Connect to a pre-existing server for collaboration.

        Arguments:
        server_ip: IP address of server to connect to
        server_port: Port of server to connect to

        Return:
        True if connection successful, False otherwise

        """

        valid_client = True

        """Check if the address could be reached!"""
        valid_address = True
        '''
	Commented out in order to allow connection to an OSX server from Windows
	OSX to Windows and Windows to Windows function with this code included
	Seems like a firewalling issue, but isn't
	try:
            socket.gethostbyaddr(server_ip)
        except socket.gaierror:
            print "@@ Invalid server address!"
            valid_address = False
            valid_client = False
        except:
            print "@@ Failed to create client!"
            valid_address = False
            valid_client = False
        '''

        """Try to open test connection to server"""
        if valid_address == True:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                test_socket.connect((server_ip, server_port))
                test_socket.shutdown(2)
            except:
                print "@@ Cannot connect test socket!"
                valid_address = False
       
        """If address reachable, then connect to server"""
        if valid_address == True:
            """Open client"""
            try:
                self.client = Client(self.music_player, self.gui, server_ip,
                                     server_port)
            except socket.gaierror:
                print "@@ Server address error. Check your input."
                valid_client = False
            except ClientNetworkError:
                print "@@ Client pipeline has error!"
                valid_client = False
            except:
                print "@@ Client creation error:", sys.exc_info()[0]
                valid_client = False

            if self.client != None and valid_client == True:
                try:
                    self.client.Loop()
                except:
                    valid_client = False
                    print "@@ Deathly error when first client loop run!"
                if valid_client == False:
                    self.client.terminate()
                    self.client = None
                    self.connected = NOT_CONNECTED

            """Create client thread if client was created"""
            if valid_client == True:
                print "@@ Valid client"
                self.client_thread = NetworkThread("client", self.client)
                self.client_thread.start()
                self.connected = NETWORK_CLIENT
        else:
            valid_client = False

        return valid_client
        
    def start_server(self, server_ip, server_port):
        """Start server
   
        Arguments:
        server_ip: IP address of server
        server_port: port on server to accept network transactions
    
        Return:
        True if server created successfully, false otherwise

        """
        valid_server = True

        """Attempt to create server"""
        try: 
            self.server = ServerObj(self.music_player, 
                                    localaddr=(server_ip, server_port))
        except socket.gaierror:
            print "@@ Error binding address. Check your input."
            valid_server = False
        except:
            print "@@ Server creation error. Please try again!"
            valid_server = False
         
        """If server created, make thread for server, and make client"""   
        if valid_server == True:
            self.server_thread = NetworkThread("server", self.server)
            self.server_thread.start()
            valid_client = self.connect_to_server(server_ip, server_port)
            if valid_client == False:
                self.destroy_server()
                valid_server = False
                self.connected = NOT_CONNECTED
            else:
                self.connected = NETWORK_SERVER
        else:
            if (self.server != None):
                self.server.terminate()
                self.server = None
        
        return valid_server

    def terminate_connections(self):
        if self.connected == NOT_CONNECTED:
            pass
        elif self.connected == NETWORK_CLIENT:
            self.destroy_client()
        elif self.connected == NETWORK_SERVER:
            self.destroy_client()
            self.destroy_server()

        self.connected = NOT_CONNECTED
 
    def destroy_server(self):
        
        if self.server != None:
            self.server.notify_end()
            self.server.Loop()
        if self.server_thread != None:
            self.server_thread.terminate()
        if self.server != None:
            self.server.terminate()

        self.server_thread = None
        self.server = None

    def destroy_client(self):
        
        if self.client != None:
            self.client.Loop()
        if self.client_thread != None:
            self.client_thread.terminate()
        if self.client != None:
            self.client.terminate()        

        self.client_thread = None
        self.client = None

    def get_server_ip(self):
        """Get IP address of the server if one is active"""
        pass
           
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

    def request_session(self):
        """Request music session from server to application's client"""
        if self.connected != NOT_CONNECTED:
            self.client.request_session()

#network testing code
if __name__ == "__main__":
    test = NetworkHandler(None, None)
    test.start_server("localhost", int(25000))
    sleep(.1)
    test.send_volume(1, 2)
    
            
