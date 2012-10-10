from ServerObj import ServerObj
from Client import Client

import sys
from sys import stdin

from pyo import *
from time import sleep

import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

def callback(instance):
    print "I was pressed!"

def run_client(instance):
    print "Connecting to a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")

def run_server(instance):
    print "Starting a server..."
    sys.stdout.write("Server?: ")
    host = stdin.readline().rstrip("\n")
    sys.stdout.write("Port?: ")
    port = stdin.readline().rstrip("\n")

class ButtonApp(App):
    def build(self):
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=150)
        button1 = Button(text='Start client', font_size=14)
        button1.bind(on_press=run_client)
        layout.add_widget(button1)
        button2 = Button(text='Start server', font_size=14)
        button2.bind(on_press=run_server)
        layout.add_widget(button2)
        return layout

if __name__ == "__main__":
    ButtonApp().run()
