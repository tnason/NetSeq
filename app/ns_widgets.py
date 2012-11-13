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
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.core.window import Window

class NSWidget(Widget):
    """Disable-able widget (absorbs clicks"""

    enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def on_touch_down(self, touch):
        if (self.enabled == True):
            Widget.on_touch_down(self, touch)
        else:
            pass

    def on_touch_move(self, touch):
        if (self.enabled == True):
            Widget.on_touch_down(self, touch)
        else:
            pass

    def on_touch_up(self, touch):
        if (self.enabled == True):
            Widget.on_touch_down(self, touch)
        else:
            pass


class NSPopup(Widget):
    """Popup class that waits for action"""

    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 300

    """State determines whether user has made selection"""
    state = OptionProperty('waiting', options=('waiting', 'done'))

    def __init__(self, title, body, options, **kwargs):
        """Construct NSPopup

        Arguments
        title: title of Popup
        body: text to comprise of Popup body
        options: dictionary of format {"option": callback, ...} -- options to
            be listed on buttons, and the function to call on option trigger

        """

        """Basic Widget constructor"""
        super(NSPopup, self).__init__(width=self.DEFAULT_WIDTH,
                                      height=self.DEFAULT_HEIGHT)

        """Store data"""
        self.options = options

        """Center popup relative to screen"""
        self.x = (Window.width - self.width) / 2
        self.y = (Window.height - self.height) / 2

        """Set formatting defaults"""
        self.size = [self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT]

        """Selection is originally nothing"""
        self.selection = None

        """Layout constants"""
        num_buttons = len(options)
        BUTTON_MAX_WIDTH = 150
        PADDING = 10
        BUTTON_BALANCED_WIDTH = (self.width - (num_buttons + 1) * 
                                 PADDING) / num_buttons
        BUTTON_WIDTH = min(BUTTON_BALANCED_WIDTH, BUTTON_MAX_WIDTH)
        BUTTON_HEIGHT = 50
        BUTTON_PADDING = (self.width - (num_buttons * BUTTON_WIDTH)) /\
                         (num_buttons + 1)
        BUTTON_TEXT_SIZE = [BUTTON_WIDTH, BUTTON_HEIGHT]
        BUTTON_FONT_SIZE = 12
        BUTTON_Y = self.y + PADDING
    
        BACKGROUND_COLOR = Color(0.2, 0.2, 0.2)
        EDGE_COLOR = Color(0.6, 0.6, 0.6)
        EDGE_WIDTH = self.width
        EDGE_HEIGHT = self.height
        EDGE_SIZE = [EDGE_WIDTH, EDGE_HEIGHT]
        BORDER_SIZE = 5
        BACKGROUND_WIDTH = EDGE_WIDTH - BORDER_SIZE * 2
        BACKGROUND_HEIGHT = EDGE_HEIGHT - BORDER_SIZE * 2
        BACKGROUND_SIZE = [BACKGROUND_WIDTH, BACKGROUND_HEIGHT]

        TITLE_HEIGHT = 50
        TITLE_WIDTH = BACKGROUND_WIDTH - PADDING
        TITLE_FONT_SIZE = 18
        TITLE_PADDING_ABOVE = 50
        TITLE_TOP = self.top - BORDER_SIZE - TITLE_PADDING_ABOVE
        TITLE_TEXT_SIZE = [TITLE_WIDTH, TITLE_HEIGHT]

        BODY_HEIGHT = self.height - PADDING - BUTTON_HEIGHT - PADDING - \
                      PADDING - TITLE_HEIGHT - PADDING
        BODY_PADDING_SIDES = 30
        BODY_WIDTH = BACKGROUND_WIDTH - PADDING - BODY_PADDING_SIDES * 2
        BODY_TEXT_SIZE = [BODY_WIDTH, BODY_HEIGHT]
        BODY_FONT_SIZE = 14

        """Create background"""
        edge = Widget()
        edge.pos = self.pos
        edge.canvas = Canvas()
        edge.canvas.add(EDGE_COLOR)
        edge_rectangle = Rectangle(size=EDGE_SIZE)
        edge_rectangle.pos = edge.pos
        edge.canvas.add(edge_rectangle)
        self.add_widget(edge)

        background = Widget()
        background.x = edge.x + BORDER_SIZE
        background.y = edge.y + BORDER_SIZE
        background.canvas = Canvas()
        background.canvas.add(BACKGROUND_COLOR)
        background_rectangle = Rectangle(size=BACKGROUND_SIZE)
        background_rectangle.pos = background.pos
        background.canvas.add(background_rectangle)
        self.add_widget(background)

        """Make a button for each option"""
        option_button_x = self.x + BUTTON_PADDING
        for option in options.keys():
            option_button = Button(text=option, width=BUTTON_WIDTH,
                                   valign='middle', halign='center',
                                   height=BUTTON_HEIGHT,
                                   text_size=BUTTON_TEXT_SIZE,
                                   font_size=BUTTON_FONT_SIZE)
            option_button.x = option_button_x
            option_button.y = BUTTON_Y
            option_button.bind(on_release=self.select_option)
            self.add_widget(option_button)            

            """Increment x for the next button"""
            option_button_x += option_button.width + BUTTON_PADDING

        """Create title label"""
        title = Label(text=title, valign='middle', halign='center',
                      text_size=TITLE_TEXT_SIZE, font_size=TITLE_FONT_SIZE,
                      TITLE=TITLE_WIDTH, height=TITLE_HEIGHT)
        title.center_x = self.center_x
        title.top = TITLE_TOP
        self.add_widget(title)

        """Create main message label"""
        body = Label(text=body, valign='top', halign='center',
                      text_size=BODY_TEXT_SIZE, font_size=BODY_FONT_SIZE,
                      BODY=BODY_WIDTH, height=BODY_HEIGHT)
        body.center_x = self.center_x
        body.top = title.y - PADDING
        self.add_widget(body)

    def select_option(self, button):
        """Perform the callback associated with the choice"""
        selection = button.text
        callback = self.options[selection]
        if callback != None:
            callback()        

        """Hide once option was selected!"""
        """XXX: Potential area for memory leaks?"""
        self.state = 'done'
        self.parent.remove_widget(self)
        self.clear_widgets()


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
