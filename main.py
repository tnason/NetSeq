import os
import platform

"""OS X needs to use a dummy clipboard, as Pygame scrap is missing"""
if platform.system() == "Windows":
    os.environ['KIVY_CLIPBOARD'] = 'pygame'
else:
    os.environ['KIVY_CLIPBOARD'] = 'dummy'

from netseq.gui import NetSeqApp

"""Kick off the application!"""
NetSeqApp().run()

