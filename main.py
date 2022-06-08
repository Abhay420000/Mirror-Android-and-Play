from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.actionbar import ActionBar
from kivy.uix.behaviors import DragBehavior
#from kivy.uix.popup import Popup

import multiprocessing

from KivyOnTop import register_topmost, unregister_topmost
from matplotlib.pyplot import title

from spop import startNC

TITLE = 'Game Controler'

class Main(FloatLayout):
    def __init__(self, maxSize, **kwargs):
        super().__init__(**kwargs)
        self.bx = BoxLayout(pos_hint={'x':0, 'y':0})
        self.bx.oreintation = 'horizontal'
        self.maxSize = maxSize
        self.bx.add_widget(Button(text = '+', on_press = self.add))
        self.bx.add_widget(Button(text = 'Clear All', on_press = self.deleteAll))
        self.bx.add_widget(Label(text = 'Game Controler'))
        self.bx.add_widget(Button(text = 'X', on_press = self.exit))
        
        self.add_widget(self.bx)
        
        self.process_list = []
        self.title_ = 0
        self.curr_pos = {}
        self.pop_size = multiprocessing.Value('i', 50)
        
        """
        Example:-
        data = {
            'size': 50,
            '0':{
                'pos': (0, 0),
                'text': None,
                'status': 'Alive',
                'process_obj': obj
            },
        }
        """
    
    def on_stop(self):
        pass    

    def add(self, abtn):
        self.title_ += 1
        self.curr_pos[self.title_] = multiprocessing.Array('i', 2)
        p1 = multiprocessing.Process(target=startNC, args=(str(self.title_), self.pop_size, self.curr_pos[self.title_]))
        p1.start()
        multiprocessing.freeze_support()
        self.process_list.append(p1)
        
    def deleteAll(self, abtn):
        print("Hello World")

    def exit(self, abtn):
        App.get_running_app().stop()


class DragBTN(DragBehavior, Button):
    def __init__(self, maxSize, text, **kwargs):
        super().__init__(**kwargs)
        self.drag_rectangle = (0,0,maxSize[0],maxSize[1])
        self.text = text
        self.drag_timeout = 1000000
        self.size_hint = (None, None)
        self.size = (30,30)
        #self.pos_hint = {'x':0, 'y':0}
        #self.pos = (maxSize[0]/2,maxSize[1]/2)

class MYApp(App):
    title: str = TITLE
    def on_start(self):
        register_topmost(Window, TITLE)
        Window.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))
        #win32gui.SetWindowLong(KivyOnTop.find_hwnd(TITLE), win32con.GWL_EXSTYLE, win32con.WS_EX_NOACTIVATE)
        Window.bind(on_cursor_enter=lambda *_: Window.raise_window())
            
    def build(self): 
        #-- maximize first, to get the screen size, minus any OS toolbars
        Window.maximize()
        maxSize = Window.system_size
        
        #-- set the actual window size, to be slightly smaller than full screen
        desiredSize = (maxSize[0]*0.35, maxSize[1]*0.035)
        Window.size = desiredSize

        #-- center the window
        Window.top = 0
        Window.left = maxSize[0]/2 - Window.system_size[0]/2
        return Main(maxSize)

if __name__ == '__main__':
    app = MYApp()
    app.run()
