from kivy.app import App
from kivy.uix.widget import Widget
from music_player import Note
from music_player import MusicPlayer
from network_handler import NetworkHandler
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle
from kivy.graphics import Color
from ns_widgets import NSToggleButton
from ns_widgets import NSSlider
import Tkinter
import tkFileDialog
import cPickle

class GUI(Widget):
    """Widget for all user interaction with sequencer"""

    def __init__(self, music_player):
        """Create main GUI

        Arguments:
        music_player -- audio generator for full application
        network -- network client and server handler

        """

        # Initialize Tkinter, and instruct it hide root window
        root = Tkinter.Tk()
        root.withdraw()

        # Perform widget initializations
        super(GUI, self).__init__()

        # OVERALL STRUCTURE
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        OUTER_PADDING = 20

        # Set default parameters to be used in accurately loading an
        # initial state to the GUI
        self.music_player = music_player
        self.track_id = MusicPlayer.WAVETABLE_A

        # For dynamic GUI coloring
        self.TRACK_COLORS = [[.7, .4, .9, 1.0], 
                             [.6, .9, .4, 1.0], 
                             [.8, .5, .3, 1.0]]
        self.colorables = []

        # BUTTON GRID
        NOTE_BUTTON_WIDTH = 48
        NOTE_BUTTON_HEIGHT = 48
        NOTE_BUTTON_PADDING = 7
        ROW_LABEL_WIDTH = 54
        ROW_LABEL_HEIGHT = NOTE_BUTTON_HEIGHT
        ROW_LABEL_FONT_SIZE = 10
        NOTE_BUTTON_ROWS = MusicPlayer.NUM_ROWS
        NOTE_BUTTON_COLS = MusicPlayer.NUM_COLS

        GRID_WIDTH = NOTE_BUTTON_PADDING + ROW_LABEL_WIDTH + \
                     NOTE_BUTTON_PADDING + (NOTE_BUTTON_COLS * 
                     (NOTE_BUTTON_WIDTH + NOTE_BUTTON_PADDING))
        GRID_HEIGHT = NOTE_BUTTON_PADDING + (NOTE_BUTTON_ROWS * 
                      (NOTE_BUTTON_HEIGHT + NOTE_BUTTON_PADDING))
        GRID_X = OUTER_PADDING
        GRID_Y = WINDOW_HEIGHT - OUTER_PADDING - GRID_HEIGHT

        PLAYHEAD_WIDTH = NOTE_BUTTON_WIDTH + 4
        PLAYHEAD_HEIGHT = GRID_HEIGHT
        PLAYHEAD_OPACITY = .5
        PLAYHEAD_COLOR = Color(1.0, 1.0, 1.0)

        # Playhead
        playhead_widget = Widget()
        playhead_canvas = Canvas()
        playhead_canvas.add(PLAYHEAD_COLOR)
        playhead = Rectangle(size=[PLAYHEAD_WIDTH, PLAYHEAD_HEIGHT])
        playhead_canvas.add(playhead)
        playhead_canvas.opacity = PLAYHEAD_OPACITY
        playhead_widget.canvas = playhead_canvas
        self.add_widget(playhead_widget)
        self.playhead = playhead

        # For each row, create labels and notes
        self.row_labels = []
        self.note_buttons = []

        row_top = GRID_Y + GRID_HEIGHT - NOTE_BUTTON_PADDING

        for row in range(0, NOTE_BUTTON_ROWS):
            col_x = GRID_X + NOTE_BUTTON_PADDING

            # Make label for row
            row_label = Label(text=str(row), width=ROW_LABEL_WIDTH, 
                              height=ROW_LABEL_HEIGHT, 
                              text_size=[ROW_LABEL_WIDTH, ROW_LABEL_HEIGHT],
                              font_size=ROW_LABEL_FONT_SIZE, halign='center',
                              valign='middle')
            row_label.x = col_x
            row_label.top = row_top
            self.add_widget(row_label)
            self.row_labels.append(row_label)

            col_x = col_x + ROW_LABEL_WIDTH + NOTE_BUTTON_PADDING
            
            # Create all buttons for row
            row_notes = []
            for col in range(0, NOTE_BUTTON_COLS):
                col_button = NSToggleButton(width=NOTE_BUTTON_WIDTH,
                                          height=NOTE_BUTTON_HEIGHT)
                col_button.id = 'row' + str(row) + ',col' + str(col)
                col_button.x = col_x
                col_button.top = row_top
                col_button.bind(on_press=self.trigger_note)
                row_notes.append(col_button)
                self.add_widget(col_button)
                self.colorables.append(col_button)
                col_x = col_x + NOTE_BUTTON_WIDTH + NOTE_BUTTON_PADDING
                
            self.note_buttons.append(row_notes)
            row_top = row_top - NOTE_BUTTON_PADDING - NOTE_BUTTON_HEIGHT

        # Set playhead start position
        leftmost_note = self.note_buttons[0][0]
        playhead_x = leftmost_note.center_x - (PLAYHEAD_WIDTH / 2)
        playhead_y = GRID_Y
        self.playhead.pos = [playhead_x, playhead_y]

        # PLAYBACK MENU
        PLAYBACK_X = OUTER_PADDING
        PLAYBACK_Y = OUTER_PADDING
        PLAYBACK_WIDTH = GRID_WIDTH
        PLAYBACK_HEIGHT = WINDOW_HEIGHT - OUTER_PADDING - GRID_HEIGHT - \
                          OUTER_PADDING - OUTER_PADDING
        PLAYBACK_CENTER_Y = PLAYBACK_Y + (PLAYBACK_HEIGHT / 2)
        PLAYBACK_TOP = PLAYBACK_Y + PLAYBACK_HEIGHT

        PLAY_BUTTON_WIDTH = 48
        PLAY_BUTTON_HEIGHT = 48
        PLAYALL_BUTTON_WIDTH = 60
        PLAYALL_BUTTON_HEIGHT = PLAY_BUTTON_HEIGHT / 2
        PLAYALL_BUTTON_FONT_SIZE = 8
        PLAYALL_BUTTON_TEXT_SIZE = [PLAYALL_BUTTON_WIDTH, 
                                    PLAYALL_BUTTON_HEIGHT]
        PAGE_BUTTON_WIDTH = 20
        PAGE_BUTTON_HEIGHT = 30
        NUM_PAGE_BUTTONS = MusicPlayer.NUM_PAGES
        PAGE_LABEL_WIDTH = (PAGE_BUTTON_WIDTH * NUM_PAGE_BUTTONS)
        PAGE_LABEL_HEIGHT = 20
        PAGE_LABEL_FONT_SIZE = 10
        PAGE_LABEL_OFFSET = 5
        TRACK_BUTTON_WIDTH = 48
        TRACK_BUTTON_HEIGHT = 48
        NUM_TRACK_BUTTONS = MusicPlayer.NUM_TRACKS
        NUM_PLAYBACK_ELEMENTS = 4
        TRACK_LABEL_WIDTH = TRACK_BUTTON_WIDTH * NUM_TRACK_BUTTONS
        TRACK_LABEL_HEIGHT = PAGE_LABEL_HEIGHT
        TRACK_LABEL_FONT_SIZE = PAGE_LABEL_FONT_SIZE
        TRACK_LABEL_TEXT_SIZE = [TRACK_LABEL_WIDTH, TRACK_LABEL_HEIGHT]
        TRACK_LABEL_OFFSET = PAGE_LABEL_OFFSET

        PLAYBACK_PADDING = (PLAYBACK_WIDTH - (PAGE_BUTTON_WIDTH * 
                            NUM_PAGE_BUTTONS) - (PLAY_BUTTON_WIDTH) - 
                            (TRACK_BUTTON_WIDTH * NUM_TRACK_BUTTONS) - 
                            PLAYALL_BUTTON_WIDTH) / (NUM_PLAYBACK_ELEMENTS + 1)
        
        # Play/pause button
        PLAY_BUTTON_X = PLAYBACK_X + PLAYBACK_PADDING
        # TODO: add a border for this button
        play_button = ToggleButton(width=PLAY_BUTTON_WIDTH, 
                             height=PLAY_BUTTON_HEIGHT)
        play_button.bind(on_press=self.play_pause)
        play_button.background_normal = \
            "assets/icons/media-playback-start-4.png"
        play_button.background_down = \
            "assets/icons/media-playback-pause-4.png"
        play_button.x = PLAY_BUTTON_X
        play_button.center_y = PLAYBACK_CENTER_Y
        self.play_button = play_button
        self.add_widget(play_button)
        self.colorables.append(play_button)

        # Buttons to play one page or all
        one_page_button = NSToggleButton(width=PLAYALL_BUTTON_WIDTH,
                                       height=PLAYALL_BUTTON_HEIGHT,
                                       text='One page',
                                       text_size=PLAYALL_BUTTON_TEXT_SIZE,
                                       font_size=PLAYALL_BUTTON_FONT_SIZE,
                                       halign='center', valign='middle')
        one_page_button.bind(on_press=self.play_one_page)
        one_page_button.x = play_button.right + PLAYBACK_PADDING
        one_page_button.top = PLAYBACK_CENTER_Y + PLAYALL_BUTTON_HEIGHT
        self.one_page_button = one_page_button
        self.add_widget(one_page_button)
        self.colorables.append(one_page_button)

        all_pages_button = NSToggleButton(width=PLAYALL_BUTTON_WIDTH,
                                        height=PLAYALL_BUTTON_HEIGHT,
                                        text='All pages', 
                                        text_size=PLAYALL_BUTTON_TEXT_SIZE,
                                        font_size=PLAYALL_BUTTON_FONT_SIZE,
                                        halign='center', valign='middle')
        all_pages_button.bind(on_press=self.play_all_pages)
        all_pages_button.x = one_page_button.x
        all_pages_button.top = PLAYBACK_CENTER_Y
        self.all_pages_button = all_pages_button
        self.add_widget(all_pages_button)
        self.colorables.append(all_pages_button)
        
        if music_player.play_all == False:
            one_page_button.state = 'down'
            all_pages_button.state = 'normal'
        elif music_player.play_all == True:
            one_page_button.state = 'normal'
            all_pages_button.state = 'down'

        # Page selection buttons
        self.page_buttons = []
        page_buttons = []
        page_label = Label(text='Page Select', text_size=[PAGE_LABEL_WIDTH, 
                           PAGE_LABEL_HEIGHT], font_size=PAGE_LABEL_FONT_SIZE,
                           width=PAGE_LABEL_WIDTH, height=PAGE_LABEL_HEIGHT,
                           halign='center', valign='middle')
        page_button_x = all_pages_button.right + PLAYBACK_PADDING
        page_label.x = page_button_x
        page_label.top = PLAYBACK_CENTER_Y - (PAGE_BUTTON_HEIGHT / 2) - \
                         PAGE_LABEL_OFFSET
        self.add_widget(page_label)
        for page_index in range(0, NUM_PAGE_BUTTONS):
            page_id = 'page' + str(page_index)
            page_button = NSToggleButton(width=PAGE_BUTTON_WIDTH,
                                       height=PAGE_BUTTON_HEIGHT, id=page_id)
            page_button.bind(on_press=self.select_page)
            page_button.x = page_button_x
            page_button.center_y = PLAYBACK_CENTER_Y
            page_buttons.append(page_button)
            self.add_widget(page_button)
            self.colorables.append(page_button)
            page_button_x += PAGE_BUTTON_WIDTH

        self.page_buttons = page_buttons

        # Select the current music player's page with the GUI
        page_buttons[music_player.page_index].state = 'down'

        # Track selection buttons
        # TODO: color these! And pages, too!

        TRACK_BUTTON_FONT_SIZE = 10
        TRACK_BUTTON_TEXT_SIZE = [TRACK_BUTTON_WIDTH, TRACK_BUTTON_HEIGHT]
        
        track_text = ["Bass", "Lead", "Drum"]
        track_buttons = []
        self.track_buttons = []
        track_button_x = page_buttons[len(page_buttons) - 1].right + \
                         PLAYBACK_PADDING
        for track_index in range(0, NUM_TRACK_BUTTONS):
            track_id = 'track' + str(track_index)
            track_button = NSToggleButton(text=track_text[track_index],
                                        width=TRACK_BUTTON_WIDTH, 
                                        height=TRACK_BUTTON_HEIGHT, id=track_id,
                                        text_size=TRACK_BUTTON_TEXT_SIZE,
                                        font_size=TRACK_BUTTON_FONT_SIZE,
                                        halign='center', valign='middle')
            track_button.bind(on_press=self.select_track)
            track_button.x = track_button_x
            track_button.center_y = PLAYBACK_CENTER_Y
            track_buttons.append(track_button)
            self.add_widget(track_button)
            track_button_x += TRACK_BUTTON_WIDTH
        
        self.track_buttons = track_buttons        
    
        # Select the current track in the GUI
        track_buttons[self.track_id].state = 'down'

        leftmost_track_button = self.track_buttons[0]

        track_label = Label(text='Instrument Select', 
                           text_size=TRACK_LABEL_TEXT_SIZE,
                           font_size=TRACK_LABEL_FONT_SIZE,
                           width=TRACK_LABEL_WIDTH, 
                           height=TRACK_LABEL_HEIGHT,
                           halign='center', valign='middle')
        track_label.x = leftmost_track_button.x
        track_label.top = leftmost_track_button.y - TRACK_LABEL_OFFSET
        # self.add_widget(track_label)

        # SETTINGS TABS
        TABS_X = OUTER_PADDING + GRID_WIDTH + OUTER_PADDING
        TABS_Y = GRID_Y
        TABS_WIDTH = WINDOW_WIDTH - OUTER_PADDING - GRID_WIDTH - \
                     OUTER_PADDING - OUTER_PADDING
        TABS_HEIGHT = GRID_HEIGHT
        
        # Element is button, label, etc. Section is vertical group of elements
        TAB_SECTION_PADDING = 20
        TAB_ELEMENT_PADDING = 10

        # Note: it's a good idea to make these tabs the size of our icons,
        # which is 48x48
        TAB_HEADER_WIDTH = 48
        TAB_HEADER_HEIGHT = TAB_HEADER_WIDTH
        TAB_HEADER_FONT_SIZE = 20
        SECTION_LABEL_FONT_SIZE = 16
        SECTION_LABEL_WIDTH = TABS_WIDTH - TAB_SECTION_PADDING * 2
        SECTION_LABEL_HEIGHT = 30
        SECTION_LABEL_TEXT_SIZE = [SECTION_LABEL_WIDTH, SECTION_LABEL_HEIGHT]
        ELEMENT_LABEL_FONT_SIZE = 10
        ELEMENT_LABEL_WIDTH = TABS_WIDTH - TAB_ELEMENT_PADDING * 2
        ELEMENT_LABEL_HEIGHT = 20
        ELEMENT_LABEL_TEXT_SIZE = [ELEMENT_LABEL_WIDTH, ELEMENT_LABEL_HEIGHT]
        TAB_CONTENT_HEIGHT = TABS_HEIGHT - TAB_HEADER_HEIGHT
        TAB_CONTENT_TOP = TABS_Y + TAB_CONTENT_HEIGHT

        # Create main tabbed panel
        tabs = TabbedPanel(tab_width=TAB_HEADER_WIDTH, 
                           tab_height=TAB_HEADER_HEIGHT, width=TABS_WIDTH, 
                           height=TABS_HEIGHT)
        tabs.x = TABS_X
        tabs.y = TABS_Y
        self.add_widget(tabs)
        self.tabs = tabs

        # Music tab (default)
        music_tab_content = Widget(width=TABS_WIDTH, height=TAB_CONTENT_HEIGHT)
        tabs.default_tab_content = music_tab_content
        tabs.default_tab.text = ""
        # TODO: make these paths absolute?
        tabs.default_tab.background_normal = \
            "assets/icons/audio-keyboard.png"
        tabs.default_tab.background_down = \
            "assets/icons/audio-keyboard-down.png"

        # Global music options
        global_music_label = Label(text='Global', 
                                   font_size=SECTION_LABEL_FONT_SIZE,
                                   width=SECTION_LABEL_WIDTH, 
                                   height=SECTION_LABEL_HEIGHT,
                                   text_size=SECTION_LABEL_TEXT_SIZE,
                                   halign='center', valign='middle')
        global_music_label.center_x = tabs.center_x
        global_music_label.top = TAB_CONTENT_TOP - TAB_SECTION_PADDING
        music_tab_content.add_widget(global_music_label)
        
        MUSIC_SLIDER_WIDTH = TABS_WIDTH - 40
        MUSIC_SLIDER_HEIGHT = 20

        # Note: these sliders buttons have a predefined height, so we are a
        # slave to that height for positioning the sliders
        global_volume_slider = NSSlider(min=MusicPlayer.MIN_VOLUME, 
                                        max=MusicPlayer.MAX_VOLUME,
                                        value=music_player.global_volume,
                                        orientation='horizontal',
                                        height=MUSIC_SLIDER_HEIGHT,
                                        width=MUSIC_SLIDER_WIDTH)
        global_volume_slider.bind(on_touch_move=self.change_global_volume)
        global_volume_slider.center_x = tabs.center_x
        global_volume_slider.top = global_music_label.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(global_volume_slider)
        self.global_volume_slider = global_volume_slider
        self.colorables.append(global_volume_slider)

        global_volume_label = Label(text='Volume',
                                    font_size=ELEMENT_LABEL_FONT_SIZE,
                                    width=ELEMENT_LABEL_WIDTH,
                                    height=ELEMENT_LABEL_HEIGHT,
                                    text_size=ELEMENT_LABEL_TEXT_SIZE,
                                    halign='center', valign='middle')
        global_volume_label.center_x = tabs.center_x
        global_volume_label.top = global_volume_slider.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(global_volume_label)
        
        global_tempo_slider = NSSlider(min=MusicPlayer.MIN_TEMPO, 
                                       max=MusicPlayer.MAX_TEMPO,
                                       value=music_player.tempo,
                                       orientation='horizontal',
                                       height=MUSIC_SLIDER_HEIGHT,
                                       width=MUSIC_SLIDER_WIDTH)
        global_tempo_slider.bind(on_touch_move=self.change_global_tempo)
        global_tempo_slider.center_x = tabs.center_x
        global_tempo_slider.top = global_volume_label.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(global_tempo_slider)
        self.global_tempo_slider = global_tempo_slider
        self.colorables.append(global_tempo_slider)

        global_tempo_label = Label(text='Tempo',
                                   font_size=ELEMENT_LABEL_FONT_SIZE,
                                   width=ELEMENT_LABEL_WIDTH,
                                   height=ELEMENT_LABEL_HEIGHT,
                                   text_size=ELEMENT_LABEL_TEXT_SIZE,
                                   halign='center', valign='middle')
        global_tempo_label.center_x = tabs.center_x
        global_tempo_label.top = global_tempo_slider.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(global_tempo_label)

        # Instrument settings
        track_music_label = Label(text='Instrument', 
                                  font_size=SECTION_LABEL_FONT_SIZE,
                                  width=SECTION_LABEL_WIDTH, 
                                  height=SECTION_LABEL_HEIGHT,
                                  text_size=SECTION_LABEL_TEXT_SIZE,
                                  halign='center', valign='middle')
        track_music_label.center_x = tabs.center_x
        track_music_label.top = global_tempo_label.y - TAB_SECTION_PADDING
        music_tab_content.add_widget(track_music_label)
        
        track_volume_initial = music_player.get_volume(self.track_id)
        track_volume_slider = NSSlider(min=MusicPlayer.MIN_VOLUME, 
                                       max=MusicPlayer.MAX_VOLUME,
                                       value=track_volume_initial,
                                       orientation='horizontal',
                                       height=MUSIC_SLIDER_HEIGHT,
                                       width=MUSIC_SLIDER_WIDTH)
        track_volume_slider.bind(on_touch_move=self.change_track_volume)
        track_volume_slider.center_x = tabs.center_x
        track_volume_slider.top = track_music_label.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(track_volume_slider)
        self.track_volume_slider = track_volume_slider
        self.colorables.append(track_volume_slider)

        track_volume_label = Label(text='Volume',
                                   font_size=ELEMENT_LABEL_FONT_SIZE,
                                   width=ELEMENT_LABEL_WIDTH,
                                   height=ELEMENT_LABEL_HEIGHT,
                                   text_size=ELEMENT_LABEL_TEXT_SIZE,
                                   halign='center', valign='middle')
        track_volume_label.center_x = tabs.center_x
        track_volume_label.top = track_volume_slider.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(track_volume_label)
        
        track_reverb_initial = music_player.get_reverb(self.track_id)
        track_reverb_slider = NSSlider(min=MusicPlayer.MIN_REVERB,
                                       max=MusicPlayer.MAX_REVERB,
                                       value=track_reverb_initial,
                                       orientation='horizontal',
                                       height=MUSIC_SLIDER_HEIGHT,
                                       width=MUSIC_SLIDER_WIDTH)
        track_reverb_slider.bind(on_touch_move=self.change_track_reverb)
        track_reverb_slider.center_x = tabs.center_x
        track_reverb_slider.top = track_volume_label.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(track_reverb_slider)
        self.track_reverb_slider = track_reverb_slider
        self.colorables.append(track_reverb_slider)

        track_reverb_label = Label(text='Reverb',
                                   font_size=ELEMENT_LABEL_FONT_SIZE,
                                   width=ELEMENT_LABEL_WIDTH,
                                   height=ELEMENT_LABEL_HEIGHT,
                                   text_size=ELEMENT_LABEL_TEXT_SIZE,
                                   halign='center', valign='middle')
        track_reverb_label.center_x = tabs.center_x
        track_reverb_label.top = track_reverb_slider.y - TAB_ELEMENT_PADDING
        music_tab_content.add_widget(track_reverb_label)

        # Network tab
        network_tab = TabbedPanelHeader()
        network_tab.text = ""
        network_tab.background_normal = \
            "assets/icons/network-wired-2.png"
        network_tab.background_down = \
            "assets/icons/network-wired-2-down.png"
        tabs.add_widget(network_tab)
        
        TEXT_INPUT_HEIGHT = 30
        PORT_INPUT_WIDTH = 70
        IP_INPUT_WIDTH = TABS_WIDTH - TAB_SECTION_PADDING - \
                         PORT_INPUT_WIDTH - TAB_ELEMENT_PADDING - \
                         TAB_SECTION_PADDING
        NETWORK_BUTTON_WIDTH = TABS_WIDTH - TAB_SECTION_PADDING * 2
        NETWORK_BUTTON_HEIGHT = 40
        NETWORK_BUTTON_FONT_SIZE = 12
        NETWORK_BUTTON_TEXT_SIZE = [NETWORK_BUTTON_WIDTH, NETWORK_BUTTON_HEIGHT]

        network_tab_content = Widget(width=TABS_WIDTH, height=TAB_CONTENT_HEIGHT)
        network_tab.content = network_tab_content

        # TODO: Initialize this will global IP
        your_ip_label = Label(text='Your IP address is: ', 
                              font_size=ELEMENT_LABEL_FONT_SIZE,
                              width=ELEMENT_LABEL_WIDTH,
                              height=ELEMENT_LABEL_HEIGHT,
                              text_size=ELEMENT_LABEL_TEXT_SIZE,
                              valign='middle')
        your_ip_label.x = TABS_X + TAB_SECTION_PADDING
        your_ip_label.top = TAB_CONTENT_TOP - TAB_SECTION_PADDING
        network_tab_content.add_widget(your_ip_label)
        self.your_ip_label = your_ip_label

        # Server startup input
        # TODO: clear these fields when clicked, and do not clear when <Enter>
        # is pressed
        server_port_input = TextInput(text='Port', width=PORT_INPUT_WIDTH,
                                      height=TEXT_INPUT_HEIGHT)
        server_port_input.x = TABS_X + TAB_SECTION_PADDING
        server_port_input.top = your_ip_label.y - TAB_ELEMENT_PADDING
        network_tab_content.add_widget(server_port_input)
        self.server_port_input = server_port_input

        server_ip_input = TextInput(text='IP Address', width=IP_INPUT_WIDTH,
                                    height=TEXT_INPUT_HEIGHT)
        server_ip_input.x = server_port_input.right + TAB_ELEMENT_PADDING
        server_ip_input.top = server_port_input.top
        network_tab_content.add_widget(server_ip_input)
        self.server_ip_input = server_ip_input

        # TODO: implement disable-able buttons for these!
        server_start_button = Button(text='Start server', 
                                     width=NETWORK_BUTTON_WIDTH,
                                     height=NETWORK_BUTTON_HEIGHT,
                                     text_size=NETWORK_BUTTON_TEXT_SIZE,
                                     font_size=NETWORK_BUTTON_FONT_SIZE,
                                     halign='center', valign='middle')
        server_start_button.bind(on_press=self.start_server)
        server_start_button.center_x = tabs.center_x
        server_start_button.top = server_ip_input.y - TAB_ELEMENT_PADDING
        network_tab_content.add_widget(server_start_button)
        self.server_start_button = server_start_button

        join_server_button = Button(text='Join server',
                                    width=NETWORK_BUTTON_WIDTH,
                                    height=NETWORK_BUTTON_HEIGHT,
                                    text_size=NETWORK_BUTTON_TEXT_SIZE,
                                    font_size=NETWORK_BUTTON_FONT_SIZE,
                                    halign='center', valign='middle')
        join_server_button.bind(on_press=self.join_server)
        join_server_button.x = server_start_button.x
        join_server_button.top = server_start_button.y - TAB_ELEMENT_PADDING
        network_tab_content.add_widget(join_server_button)
        self.join_server_button = join_server_button

        end_connection_button = Button(text='End connection',
                                       width=NETWORK_BUTTON_WIDTH,
                                       height=NETWORK_BUTTON_HEIGHT,
                                       text_size=NETWORK_BUTTON_TEXT_SIZE,
                                       font_size=NETWORK_BUTTON_FONT_SIZE,
                                       halign='center', valign='middle')
        end_connection_button.bind(on_press=self.end_connection)
        end_connection_button.x = server_start_button.x
        end_connection_button.top = join_server_button.y - TAB_ELEMENT_PADDING
        network_tab_content.add_widget(end_connection_button)
        self.end_connection_button = end_connection_button
        
        # System options tab
        system_tab = TabbedPanelHeader()
        system_tab.background_normal = \
            "assets/icons/media-floppy.png"
        system_tab.background_down = \
            "assets/icons/media-floppy-down.png"
        tabs.add_widget(system_tab)

        system_tab_content = Widget(width=TABS_WIDTH, height=TAB_CONTENT_HEIGHT)
        system_tab.content = system_tab_content

        NUM_SYSTEM_BUTTONS = 3
        SYSTEM_BUTTON_PADDING = 20
        SYSTEM_BUTTON_FONT_SIZE = 24
        SYSTEM_BUTTON_WIDTH = TABS_WIDTH - SYSTEM_BUTTON_PADDING * 2
        SYSTEM_BUTTON_HEIGHT = (TAB_CONTENT_HEIGHT - SYSTEM_BUTTON_PADDING *
                               (NUM_SYSTEM_BUTTONS + 1)) / NUM_SYSTEM_BUTTONS
        SYSTEM_BUTTON_TEXT_SIZE = [SYSTEM_BUTTON_WIDTH, SYSTEM_BUTTON_HEIGHT]

        # Load button
        load_button = Button(text='Load', width=SYSTEM_BUTTON_WIDTH,
                             height=SYSTEM_BUTTON_HEIGHT,
                             text_size=SYSTEM_BUTTON_TEXT_SIZE,
                             font_size=SYSTEM_BUTTON_FONT_SIZE,
                             halign='center', valign='middle')
        load_button.bind(on_press=self.load_file)
        load_button.center_x = tabs.center_x
        load_button.top = TAB_CONTENT_TOP - SYSTEM_BUTTON_PADDING
        system_tab_content.add_widget(load_button)        

        # Save button
        save_button = Button(text='Save', width=SYSTEM_BUTTON_WIDTH,
                             height=SYSTEM_BUTTON_HEIGHT,
                             text_size=SYSTEM_BUTTON_TEXT_SIZE,
                             font_size=SYSTEM_BUTTON_FONT_SIZE,
                             halign='center', valign='middle')
        save_button.bind(on_press=self.save_file)
        save_button.center_x = tabs.center_x
        save_button.top = load_button.y - SYSTEM_BUTTON_PADDING
        system_tab_content.add_widget(save_button)        

        # Quit button
        quit_button = Button(text='Quit', width=SYSTEM_BUTTON_WIDTH,
                             height=SYSTEM_BUTTON_HEIGHT,
                             text_size=SYSTEM_BUTTON_TEXT_SIZE, 
                             font_size=SYSTEM_BUTTON_FONT_SIZE,
                             halign='center', valign='middle')
        quit_button.center_x = tabs.center_x
        quit_button.top = save_button.y - SYSTEM_BUTTON_PADDING
        system_tab_content.add_widget(quit_button)        

        # APPLICATION TITLE
        TITLE_WIDTH = TABS_WIDTH
        TITLE_HEIGHT = 50
        TITLE_TEXT_SIZE = [TITLE_WIDTH, TITLE_HEIGHT]
        TITLE_FONT_SIZE = 30
        SUBTITLE_WIDTH = TITLE_WIDTH
        SUBTITLE_HEIGHT = 30
        SUBTITLE_TEXT_SIZE = [SUBTITLE_WIDTH, SUBTITLE_HEIGHT]
        SUBTITLE_FONT_SIZE = 15
        TITLE_X = TABS_X

        title_label = Label(text='NetSeq', width=TITLE_WIDTH,
                            height=TITLE_HEIGHT, halign='center', 
                            valign='middle', text_size=TITLE_TEXT_SIZE,
                            font_size=TITLE_FONT_SIZE)
        title_label.top = PLAYBACK_TOP
        title_label.x = TITLE_X
        self.add_widget(title_label)

        subtitle_label = Label(text='Music with Friends',
                               width=SUBTITLE_WIDTH,
                               height=SUBTITLE_HEIGHT,  
                               text_size=SUBTITLE_TEXT_SIZE,
                               font_size=SUBTITLE_FONT_SIZE,
                               halign='center', valign='middle')
        subtitle_label.top = title_label.y
        subtitle_label.x = TITLE_X
        self.add_widget(subtitle_label)

        # Finishing steps
        self.set_color(self.track_id)
        self.reload_row_labels()

    def __del__(self):
        """Destroy this instance of the GUI"""
        pass

    def set_note(self, note):
        """Set a note in note grid to on or off

        Arguments:
        note -- note with position in GUI and whether to turn on

        """
        if note.page_index == self.music_player.page_index and note.track_id ==\
           self.track_id:
           if note.turn_on == True:
               self.note_buttons[note.row][note.column].state = 'down'
           elif note.turn_on == False:
               self.note_buttons[note.row][note.column].state = 'normal'
        

    def set_volume(self, track_index, volume):
        """Redraw volume slider for a track at new value

        Arguments:
        track_index -- which track to set slider for
        volume -- new volume for the track

        """
        # Only visually change the volume slider if the current track is the
        # same as that for which volume has changed
        if track_index == self.track_id:
            self.track_volume_slider.value = volume

    def set_reverb(self, track_index, reverb):
        """Redraw rever slider for a track at new value

        Arguments:
        track_index -- which track to redraw slider for
        reverb -- new value for reverb

        """
        # Only visually change the reverb slider if the current track is the
        # same as that for which reverb has changed
        if track_index == self.track_id:
            self.track_reverb_slider.value = reverb

    def set_tempo(self, tempo):
        """Redraw global tempo at new value

        Arguments:
        tempo -- new value for tempo

        """
        self.global_tempo_slider.value = tempo

    def new_session(self):
        """Redraw entirety of UI in response to session load"""
        self.reload_notes()
        self.reload_sliders()

    def update_playhead(self):
        """Move playhead to new column

        Arguments:
        column -- destination column for playhead
        
        """
        playhead_width = self.playhead.size[0]
        OFFSCREEN_X = playhead_width * -1
        beat_index = self.music_player.beat_index
        beat_page = beat_index / self.music_player.NUM_ROWS
        playhead_index = self.music_player.playhead_index
        # Only show the playhead if you are currently on a page
        # that holds the current MusicPlayer beat
        if beat_page == self.music_player.page_index:
            column_note_button = self.note_buttons[0][playhead_index]
            playhead_x = column_note_button.center_x -\
                         (playhead_width / 2)
        else:
            playhead_x = OFFSCREEN_X

        self.playhead.pos = [playhead_x, self.playhead.pos[1]]

    def break_from_server(self):
        """Show window describing disconnected server"""
        pass

    def add_network_handler(self, network_handler):
        """Make sure this is called after init, before using the GUI"""
        self.network_handler = network_handler


    """Internal methods"""
    """ XXX 
        Buttons utilize a Kivy glitch where the callback takes two
        arguments, typically (instance, value). Having a call to a 'self'
        function pushes instance to the second value.
        Maybe one day if Kivy changes this could break the operation of our
        ToggleButtons if the order in which parameters are sent changes
    """

    """GUI helpers"""
    def set_color(self, color_index):
        # Color all 'neutral' elements
        new_color = self.TRACK_COLORS[color_index]
        for colorable in self.colorables:
            colorable.background_color = new_color

        # Color currently-selected track button
        for track_index in range(0, len(self.track_buttons)):
            track_button = self.track_buttons[track_index]
            if track_index == self.track_id:
                track_button.background_color = self.TRACK_COLORS[track_index]
            else:
                track_button.background_color = [1.0, 1.0, 1.0, 1.0]

    """Network functions"""
    def start_server(self, button):
        server_ip = self.server_ip_input.text
        server_port = int(self.server_port_input.text)
        self.network_handler.start_server(server_ip, server_port)        

    def join_server(self, button):
        server_ip = self.server_ip_input.text
        server_port = int(self.server_port_input.text)
        self.network_handler.connect_to_server(server_ip, server_port)

    def end_connection(self, button):
        self.network_handler.terminate_connections()
            
    """System functions"""
    def load_file(self, button):
        load_types = [ ('NetSeq files', '*.ns')]
        filename = tkFileDialog.askopenfilename(defaultextension='.ns', 
                                                title='Load Session',
                                                filetypes=load_types)

        if filename != '':
            try:
                file = open(filename, 'r')
                file_valid = True
            except IOError:
                print "Invalid filename!"
                file_valid = False
        else:
            file_valid = False        

        if file_valid == True:
            session = cPickle.load(file)
            self.music_player.set_session(session)
            self.new_session()

    def save_file(self, button):
        filename = tkFileDialog.asksaveasfilename(defaultextension='.ns',
                                                  initialfile='my_session',
                                                  title='Save Session')
        if filename != '':
            session = self.music_player.get_session()
            file = open(filename, 'w')
            cPickle.dump(session, file)

    def exit(self, button):
        pass

    """Music functions"""
    def trigger_note(self, button):

        button_id = button.id
        row_str, col_str = button_id.split(',')
        row_index = int(row_str.replace('row', ''))
        col_index = int(col_str.replace('col', ''))

        if button.state == 'down':
            turn_on = True
        elif button.state == 'normal':
            turn_on = False

        trigger_data = Note(self.track_id, self.music_player.page_index,
                            col_index, row_index, turn_on)

        self.music_player.set_note(trigger_data)
        self.network_handler.send_note(trigger_data)
    
    """ Functions for GUI to change fields within the MusicPlayer and those
        of other clients through network """
    def change_global_volume(self, slider, value):
        self.music_player.set_global_volume(slider.value)

    def change_global_tempo(self, slider, value):
        self.music_player.set_tempo(slider.value)
        self.network_handler.send_tempo(slider.value)

    def change_track_volume(self, slider, value):
        self.music_player.set_volume(self.track_id, slider.value)
        self.network_handler.send_volume(slider.value, self.track_id)

    def change_track_reverb(self, slider, value):
        self.music_player.set_reverb(self.track_id, slider.value)
        self.network_handler.send_reverb(slider.value, self.track_id)

    def select_page(self, button):
        # On press: deselect all other selected pages so only on is selected
        if button.state == 'down':
            button_id = button.id
            page_select_index = int(button_id.replace('page', ''))
            for page_index in range(0, len(self.page_buttons)):
                if page_index != page_select_index:
                    page_button = self.page_buttons[page_index]
                    page_button.state = 'normal'
            self.music_player.page_index = page_select_index
            self.reload_notes()
            self.update_playhead()
        # If user tries to de-select current page, don't let them!
        elif button.state == 'normal':
            button.state = 'down'

    def select_track(self, button):
        # On press...
        if button.state == 'down':
            button_id = button.id
            track_select_index = int(button_id.replace('track', ''))
            # Deselect other tracks
            for track_index in range(0, len(self.track_buttons)):
                if track_index != track_select_index:
                    track_button = self.track_buttons[track_index]
                    track_button.state = 'normal'
            # Update GUI to reflect new track
            self.track_id = track_select_index
            self.reload_notes()
            self.reload_row_labels()
            self.reload_sliders()
            self.set_color(track_select_index)
        # On deselection, keep the button pressed
        elif button.state == 'normal':
            button.state = 'down'

    def reload_row_labels(self):
        row_text = self.music_player.get_names(self.track_id)
        for row_index in range(0, self.music_player.NUM_ROWS):
            row_label = self.row_labels[row_index]
            row_label.text = row_text[row_index]            

    def reload_notes(self):
        # Reset button appearance to match which notes on page are selected
        notes = self.music_player.get_current_page(self.track_id)
        for row_index in range(0, self.music_player.NUM_ROWS):
            for col_index in range(0, self.music_player.NUM_COLS):
                note_value = notes[row_index][col_index]
                if note_value == 0:
                    self.note_buttons[row_index][col_index].state = 'normal'
                elif note_value == 1:
                    self.note_buttons[row_index][col_index].state = 'down'

    def reload_sliders(self):
        track_volume = self.music_player.get_volume(self.track_id)
        track_reverb = self.music_player.get_reverb(self.track_id)
        tempo = self.music_player.get_tempo()
        self.track_volume_slider.value = track_volume
        self.track_reverb_slider.value = track_reverb
        self.global_tempo_slider.value = tempo

    def play_pause(self, button):
        if button.state == 'down':
            self.music_player.play()
        elif button.state == 'normal':
            self.music_player.pause()

    def play_all_pages(self, button):
        # Deselect one-page button, set music player to play all
        if button.state == 'down':
            self.one_page_button.state = 'normal'
            self.music_player.play_all = True
        # Consecutive presses: do nothing
        elif button.state == 'normal':
            button.state = 'down'

    def play_one_page(self, button):
        # Deselect all-pages button, set music player to play one page
        if button.state == 'down':
            self.all_pages_button.state = 'normal'
            self.music_player.play_all = False
        # Consecutive presses: do nothing
        elif button.state == 'normal':
            button.state = 'down'

class NetSeqApp(App):
    """Kivy application that kicks off GUI"""
    
    def build(self):
        """Build GUI"""
        music_player = MusicPlayer()
        gui_widget = GUI(music_player)
        music_player.add_gui(gui_widget)
        network_handler = NetworkHandler(music_player, gui_widget)
        music_player.add_network_handler(network_handler)
        gui_widget.add_network_handler(network_handler)
        return gui_widget

if __name__ == "__main__":
    NetSeqApp().run()
