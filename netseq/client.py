#client module file
from time import sleep
from music_player import MusicPlayer
from PodSixNet.Connection import connection, ConnectionListener
from sys import exit
import cPickle

class Client(ConnectionListener):
    """Client for recieving music data"""    

    def __init__(self, music_player, gui, host, port):
        """Create new client"""
        self.music_player = music_player
        self.gui = gui
        self.Connect((host, port))

    def __del__(self):
        pass

    def Loop(self):
        connection.Pump()
        self.Pump()

    """Called by NetworkHandler (wrapper)"""
    def send_note(self, note):
        """function call to send note data to server"""
        note_str = cPickle.dumps(note)
        connection.Send({"action": "send_note", "note_string": note_str})

    def send_volume(self, volume, track_id):
        connection.Send({"action": "send_volume", "volume_data": volume, "track_id": track_id})

    def send_tempo(self, tempo):
        connection.Send({"action": "send_tempo", "tempo_data": tempo})

    def send_reverb(self, reverb, track_id):
        connection.Send({"action": "send_reverb", "reverb_data": reverb, "track_id": track_id})

    def send_session(self, session):
        session_string = cPickle.dumps(session)
        connection.Send({"action": "send_session", "session_string": session_string})

    def request_session(self):
        connection.Send({"action": "request_session"})

    def terminate(self):
        print "@@ Terminating client!"
        self.Loop()
        connection.Close()

    """Called by Server"""
    def Network_set_note(self, data):
        """callback for network triggered note addition"""
        #data['note_data'] = note

        note_data = cPickle.loads(data['note_string'])  
        self.music_player.set_note(note_data)
        self.gui.set_note(note_data)

    def Network_set_volume(self, data):
        """callback for network triggered volume change"""
        self.music_player.set_volume(data['track_id'], data['volume_data'])
        self.gui.set_volume(data['track_id'], data['volume_data'])
        pass

    def Network_set_tempo(self, data):
        """callback for network triggered tempo change"""
        self.music_player.set_tempo(data['tempo_data'])
        self.gui.set_tempo(data['tempo_data'])
        pass

    def Network_set_reverb(self, data):
        """callback for network triggered reverb change"""
        self.music_player.set_reverb(data['track_id'], data['reverb_data'])
        self.gui.set_reverb(data['track_id'], data['reverb_data'])
        pass

    def Network_set_session(self, data):
        """callback for network triggered session load"""
        session_data = cPickle.loads(data['session_string'])
        self.music_player.set_session(session_data)
        self.gui.new_session()

    def Network_request_session_change(self, data):
        self.gui.load_server_session()

    #built in Network events
    def Network_connected(self, data):
        print "You are now connected to the server"
	
    def Network_error(self, data):
        print 'error:', data['error'][1]
        raise ClientNetworkError
        # connection.shutdown()
        # connection.Close()
	
    def Network_disconnected(self, data):
        print '@@ Server disconnected'
    
    def Network_server_shutdown(self, data):
        self.gui.break_from_server()


class ClientNetworkError(BaseException):
    """Error in creating or operating client!"""
