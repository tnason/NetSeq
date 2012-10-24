#client module file
import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    
    def __init__(self, music_player, gui, host, port):
            self.Connect((host, port))
            self.music_player = music_player
            self.gui = gui
            print "##client started"

    def __del__(self):
        pass

    def Loop(self):
            connection.Pump()
            self.Pump()

    def send_note(self, note):
        """function call to send note data to server"""
        connection.Send({"action": "send_note", "note_data": note})

    def send_volume(self, volume, track_id):
        connection.Send({"action": "send_volume", "volume_data": volume, "track_id": track_id})

    def send_tempo(self, tempo):
        connection.Send({"action": "send_tempo", "tempo_data": tempo})

    def send_reverb(self, reverb, track_id):
        connection.Send({"action": "send_reverb", "reverb_data": reverb, "track_id": track_id})

    def send_session(self, session):
        connection.Send({"action": "send_session", "session_data": session})

    #Network events
    def Network_set_note(self, data):
        """callback for network triggered note addition"""
        #data['note_data'] = Note
        
        
        #tell the GUI to add the note
        pass
        

    def Network_set_volume(self, data):
        """callback for network triggered volume change"""
        #data['volume_data'] = volume
        #data['track_id'] = track_id
        print "volume: " + str(data['volume_data'])
        print "track id: " + str(data['track_id'])
        
        #tell the music player to change volume
        #tell the GUI to change volume
        pass

    def Network_set_tempo(self, data):
        """callback for network triggered tempo change"""
        #data['tempo_data'] = tempo
        
        #tell the music player to change tempo
        #tell the GUI to change tempo
        pass

    def Network_set_reverb(self, data):
        """callback for network triggered reverb change"""
        #data['reverb_data'] = reverb
        #data['track_id'] = track_id

        #tell the music player to change reverb
        #tell the GUI to change reverb
        pass

    def Network_set_session(self, data):
        """callback for network triggered session load"""
        #data['session_data'] = session
        
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

