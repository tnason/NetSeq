#python module for a PodSixNet 'chat' server
import sys
from time import sleep
from weakref import WeakKeyDictionary
from music_player import MusicPlayer
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import cPickle


class ClientChannel(Channel):
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
                    c.Send({"action": "set_session", "session_data": data['session_data']})            

class ServerObj(Server):
        channelClass = ClientChannel

        def __init__(self, music_player, *args, **kwargs):
            Server.__init__(self, *args, **kwargs)
            self.clients = WeakKeyDictionary() #Store weak references to clients
            self.music_player = music_player
            print 'Server launched'

        def Connected(self, channel, addr):
            self.AddClient(channel)
            """New client gets server's music player session"""
            session_data = cPickle.dumps(self.music_player.get_session())
            channel.Send({"action": "set_session", "session_data": session_data})

        def AddClient(self, client):
            print "New client at " + str(client.addr)
            self.clients[client] = True
            print "clients", [c for c in self.clients]

        def DelClient(self, client):
            print "Deleting " + str(client.addr)
            del self.clients[client]

        def Broadcast(self, data):
            [c.Send(data) for c in self.clients]

        def Loop(self):
            self.Pump()

        def run_loop(self):
            self.Run()

        def Run(self):
            while True:
                    self.Pump()
                    sleep(0.0001)
        
