from music_player import MusicPlayer

import socket
import asyncore
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import sys
from time import sleep
import cPickle
from weakref import WeakKeyDictionary

class ClientChannel(Channel):
    """Channel over which data is sent by the server"""
 
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelClient(self)

    # Network functions
    def Network_send_note(self, data):
        """rebroadcast a send note command from a client to all others"""
        for c in self._server.clients:
            if c != self:
                c.Send({"action": "set_note", "note_string": data['note_string']})

    def Network_send_volume(self, data):
        """rebroadcast a send volume command from a client to all others"""
        for c in self._server.clients:
            if c != self:
                c.Send({"action": "set_volume", "volume_data": data['volume_data'], "track_id": data['track_id']})

    def Network_send_tempo(self, data):
        """rebroadcast a send tempo command from a client to all others"""
        for c in self._server.clients:
            if c != self:
                c.Send({"action": "set_tempo", "tempo_data": data['tempo_data']})

    def Network_send_reverb(self, data):
        """rebroadcast a send reverb command from a client to all others"""
        for c in self._server.clients:
            if c != self:
                c.Send({"action": "set_reverb", "reverb_data": data['reverb_data'], "track_id": data['track_id']})

    def Network_send_session(self, data):
        """rebroadcast a send session command from a client to all others"""
        for c in self._server.clients:
            if c != self:
                c.Send({"action": "request_session_change"})

    def Network_request_session(self, data):
        """Send a client server's music session"""
        session = self._server.music_player.get_session()
        session_string = cPickle.dumps(session)
        self.Send({"action": "set_session", "session_string": session_string})


class ServerObj(Server):
    """Primary 'server', or authority of network interations"""
 
    channelClass = ClientChannel

    def __init__(self, music_player, channelClass=None, 
                 localaddr=("127.0.0.1", 31425), listeners=5):
        """Construct new Server object.

        Adapted heavily from the primary 'Server' constructor
        within PodSixNet source

        """

        self.clients = WeakKeyDictionary()
        self.music_player = music_player
        if channelClass:
            self.channelClass = channelClass
       
        # asyncore setup
        self._map = {}
        self.channels = []
        asyncore.dispatcher.__init__(self, map=self._map)

        # Create socket for communications
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr()
        
        # self.bind(localaddr)
        # Attempt to bind to requested address
        try:
            self.bind(localaddr)
        except:
            print "@@ Error caught in server creation"
            self.close()
            raise

        # Start listenting
        self.listen(listeners)

    def notify_end(self):
        self.Broadcast({"action": "server_shutdown"})
        self.Loop()

    def terminate(self):
        """Destroy server cleanly"""
        print "@@ In server 'terminate'"
        self.close()

    def Connected(self, channel, addr):
        self.AddClient(channel)
        """New client gets server's music player session"""
        session_string = cPickle.dumps(self.music_player.get_session())
        channel.Send({"action": "set_session", 
                      "session_string": session_string})

    def AddClient(self, client):
        print "@@ New client at " + str(client.addr)
        self.clients[client] = True
        print "@@ clients", [c for c in self.clients]

    def DelClient(self, client):
        print "@@ Deleting " + str(client.addr)
        del self.clients[client]

    def Broadcast(self, data):
        [c.Send(data) for c in self.clients]

    def Loop(self):
        self.Pump()

