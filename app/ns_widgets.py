"""
GUI Widgets for NetSeq

Simple extensions to Kivy widgets. For graphical purposes, for widgets that
define their appearance in their module file rather than in the style
'netseq.kv' file

"""

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.properties import ListProperty
from kivy.properties import OptionProperty
from kivy.uix.textinput import TextInput

class NSTextInput(TextInput):
    """TextInput that can be enabled and disabled"""

    DISABLED_COLOR = [0.5, 0.5, 0.5, 1.0]
    ENABLED_COLOR = [1.0, 1.0, 1.0, 1.0]

    def __init__(self, **kwargs):
        TextInput.__init__(self, **kwargs)
        self.enable()

    def enable(self):
        self.enabled = True
        self.background_color = self.ENABLED_COLOR

    def disable(self):
        self.enabled = False
        self.background_color = self.DISABLED_COLOR
        self.focus = False

    def on_touch_down(self, touch):
        """Process click-down"""
        if self.enabled == True:
            TextInput.on_touch_down(self, touch)
        else:
            pass

    def on_touch_move(self, touch):
        """Process moving touch"""
        if self.enabled == True:
            TextInput.on_touch_move(self, touch)
        else:
            pass

    def on_touch_up(self, touch):
        """Process touch release"""
        if self.enabled == True:
            TextInput.on_touch_up(self, touch)
        else:
            pass       


class NSToggleButton(ToggleButton):
    """ToggleButton with gray appearance"""

    background_normal = 'atlas://assets/images/netseq-theme/button'
    background_down = 'atlas://assets/images/netseq-theme/button_pressed'


class NSSlider(Slider):
    """Slider with coloring options"""

    background_color = ListProperty([1, 1, 1, 1])


class NSDisableButton(Button):
    """Button that can be enabled and disabled"""

    DISABLED_BUTTON_COLOR = [0.5, 0.5, 0.5, 0.5]
    ENABLED_BUTTON_COLOR = [1.0, 1.0, 1.0, 1.0]
    DISABLED_TEXT_COLOR = "777777"
    ENABLED_TEXT_COLOR = "ffffff"

    state = OptionProperty('normal', options=('normal', 'down', 'disabled'))

    background_normal = 'atlas://assets/images/netseq-theme/button'
    background_down = 'atlas://assets/images/netseq-theme/button_pressed'
    background_disabled = 'atlas://assets/images/netseq-theme/button_pressed'

    def __init__(self, **kwargs):
        """Create new NSDisableButton"""
        Button.__init__(self, **kwargs)
        self.default_text = "[color=%s]" + self.text + "[/color]"
        self.markup = True
        self.enable()

    def enable(self):
        """Enable button operation"""
        self.state = 'normal'
        self.background_color = self.ENABLED_BUTTON_COLOR
        self.text = self.default_text % (self.ENABLED_TEXT_COLOR)
        self.enabled = True

    def disable(self):
        """Lock button, refusing to process press activity"""
        self.state = 'disabled'
        self.background_color = self.DISABLED_BUTTON_COLOR
        self.text = self.default_text % (self.DISABLED_TEXT_COLOR)
        self.enabled = False

    def on_touch_down(self, touch):
        """Process click-down"""
        if self.enabled == True:
            Button.on_touch_down(self, touch)
        else:
            pass

    def on_touch_move(self, touch):
        """Process moving touch"""
        if self.enabled == True:
            Button.on_touch_move(self, touch)
        else:
            pass

    def on_touch_up(self, touch):
        """Process touch release"""
        if self.enabled == True:
            Button.on_touch_up(self, touch)
        else:
            pass
