from ServerObj import ServerObj
from Client import Client

import sys
from sys import stdin

from pyo import *
from time import sleep

from thread import *

import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

layout = None
main_app = None
s = None
c = None

def run_client(instance):
    global c
    main_app.switch_UI()
    print "Connecting to a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")
    #spawn client thread
    c = Client(host, int(port))

    client_thread = start_new_thread(c.run_loop, ())
    
    
def run_server(instance):
    global s
    global c
    main_app.switch_UI()
    print "Starting a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")
    #spawn server thread
    s = ServerObj(localaddr=(host, int(port)))
    #spawn client thread
    c = Client(host, int(port))

    client_thread = start_new_thread(c.run_loop, ())
    server_thread = start_new_thread(s.run_loop, ())
 
    
def send_sound(instance):
    c.send_frequency()
        
class ClientServerChoice(App):
    def build(self):
        self.layout = GridLayout(cols=2, row_force_default=True, row_default_height=150)
        button1 = Button(text='Start client', font_size=14)
        button1.bind(on_press=run_client)
        self.layout.add_widget(button1)
        button2 = Button(text='Start server', font_size=14)
        button2.bind(on_press=run_server)
        self.layout.add_widget(button2)
        #TO KEEP GARBAGE COLLECTOR OFF OUR LAYOUT
        layout = self.layout
        print '-------------build---------------'
        print layout
        return self.layout

    def switch_UI(self):
        print '-------------test--------------'
        print self.layout
        self.layout.clear_widgets()
        print self.layout
        #self.layout = BoxLayout(orientation='vertical')
        button1 = Button(text='Send sound', font_size=14)
        button1.bind(on_press=send_sound)
        self.layout.add_widget(button1)
        
        

if __name__ == "__main__":
    main_app = ClientServerChoice()
    main_app.run()
    
