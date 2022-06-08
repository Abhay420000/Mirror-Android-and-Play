def startNC(TITLE, sizen, curr_pos):
    size = sizen.value
    #size = sizen
    from KivyOnTop import register_topmost, unregister_topmost

    #For Click and Initial Window Positioning
    import pyautogui
    screenWidth, screenHeight = pyautogui.size()

    #For changing Window Shape
    from kivy.resources import resource_find
    alpha_shape = resource_find(f'./Bubbles/{size}x{size}.png')

    from kivy.config import Config
    Config.set('graphics', 'shaped', 1)
    Config.set('graphics', 'height', size)
    Config.set('graphics', 'width', size)
    Config.set('kivy', 'window_shape', alpha_shape)

    #For GUI
    from kivy.app import App
    from kivy.uix.textinput import TextInput
    from kivy.core.window import Window
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    from kivy.metrics import dp, sp

    #Setting initial position
    Window.top = int(screenHeight/2 - size/2)
    Window.left = int(screenWidth/2 - size/2)

    class MB(Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_interval(self.setPOS, 0.1)
            self.txt = TextInput(halign = 'center',multiline=False,background_color = (1,0,0,0.5),on_text_validate = self.on_text_validate,  size = (size, size), pos = (0,0))
            
            if (size == 100):
                self.txt.font_size = sp(75)
            elif (size == 75):
                self.txt.font_size = sp(50)
            elif (size == 50):
                self.txt.font_size = sp(30)
            elif (size == 30):
                self.txt.font_size = sp(15)
            elif (size == 25):
                self.txt.font_size = sp(11)
            else:
                self.txt.text = '!'
            
            self.add_widget(self.txt)
            
            self._keyboard = Window.request_keyboard(self._keyboard_close, self)
            self._keyboard.bind(on_key_up=self.del_it)
        
        def setPOS(self, _utk):
            pass
        
        def _keyboard_close(self, *args):
            #The active keyboard is being closed.
            if self._keyboard:
                self._keyboard.unbind(on_key_up=self.del_it)
                self._keyboard = None
            
        def del_it(self, keyboard, keycode, *args):
            if isinstance(keycode, tuple):
                #print(keycode)
                keycode = keycode[1]
            if keycode == 'delete':
                #closing application
                App.get_running_app().stop()
                #removing window
                Window.close()
                
        def on_text_validate(self, Wid):
            """
            Fired when user press Enter to Validate the text.
            """
            if len(self.txt.text) != 1:
                self.txt.text = ""
                self.txt.hint_text = "?"
                self.txt.foreground_color = (0,0,0,1)
                self.txt.background_color = (1,0,0,0.5)
            else:
                self.txt.foreground_color = (1,1,1,1)
                self.txt.background_color = (0,0,0,0)
                if self.txt.text.isalpha() and self.txt.text.islower():
                    self.txt.text = self.txt.text.upper()
                self.txt.disabled_foreground_color = (1,1,1,1)
                self.txt.disabled = True
                
            self._keyboard = Window.request_keyboard(self._keyboard_close, self)
            self._keyboard.bind(on_key_up=self.del_it)

        def topwin(self, _utk):
            pass
            #Window.focus = True

        def on_touch_move(self, touch):
            """
            Place window in position choosen by user
            Args:
                touch : Gives Current Touch position inside Window
            """
            mouse_pos = pyautogui.position()
            Window.top, Window.left = mouse_pos[1] - Window.size[1]/2, mouse_pos[0] - Window.size[0]/2
            
    class MApp(App):
        title: str = TITLE
        def on_start(self):
            register_topmost(Window, TITLE)
            Window.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))
            Window.bind(on_cursor_enter=lambda *_: Window.raise_window())
        
        def on_stop(self):
            #Tell Main Process to Stop
            print("Hello World")
        
        def build(self):
            #print(Config.get('graphics', 'shaped'))
            Window.size = (size, size)
            #Config.set('graphics', 'shaped', 1)
            #Config.set('kivy', 'window_shape', alpha_shape)
            Window.shape_image = alpha_shape
            Window.shape_mode = 'binalpha'
            Window.borderless = True
            return MB()

    MApp().run()

if __name__ == '__main__':
    startNC('A', 50, 1)