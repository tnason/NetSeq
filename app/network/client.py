#client module file
import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    
    def __init__(self, host, port):
            self.Connect((host, port))
            print "client started"

    def __del__(self):
        pass

    def Loop(self):
            connection.Pump()
            self.Pump()

    def send_note(self, data):
        """function call to send note data to server"""
        connection.Send({"action": "send_note", "note_data": data})

    def send_volume(self, data):
        connection.Send({"action": "send_volume", "volume_data": data})

    def send_tempo(self, data):
        connection.Send({"action": "send_tempo", "tempo_data": data})

    def send_reverb(self, data):
        connection.Send({"action": "send_reverb", "reverb_data": data})

    def send_session(self, data):
        connection.Send({"action": "send_session", "session_data": data})

    #Network events
    def Network_set_note(self, data):
        """callback for network triggered note addition"""
        #tell the music player to add the note
        #tell the GUI to add the note
        pass
        

    def Network_set_volume(self, data):
        """callback for network triggered volume change"""
        #tell the music player to change volume
        #tell the GUI to change volume
        pass

    def Network_set_tempo(self, data):
        """callback for network triggered tempo change"""
        #tell the music player to change tempo
        #tell the GUI to change tempo
        pass

    def Network_set_reverb(self, data):
        """callback for network triggered reverb change"""
        #tell the music player to change reverb
        #tell the GUI to change reverb
        pass

    def Network_set_session(self, data):
        """callback for network triggered session load"""
        #tell the music player to load a session
        #tell the GUI to reload the session
        pass

    #built in Network events
    def Network_connected(self, data):
    	print "You are now connected to the server"
	
    def Network_error(self, data):
	print 'error:', data['error'][1]
	connection.Close()
	
    def Network_disconnected(self, data):
	print 'Server disconnected'
	exit()

