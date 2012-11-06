"""
GUI Widgets for NetSeq

Simple extensions to Kivy widgets. For graphical purposes, for widgets that
define their appearance in their module file rather than in the style
'netseq.kv' file

"""

from kivy.uix.togglebutton import ToggleButton

class NSToggleButton(ToggleButton):
    """ToggleButton with gray appearance"""

    background_normal = 'atlas://assets/images/netseq-theme/button'
    background_down = 'atlas://assets/images/netseq-theme/button_pressed'
