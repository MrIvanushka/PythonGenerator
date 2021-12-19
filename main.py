from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from MapRenderer import InitRenderer
from Player import Player
from kivy.uix.screenmanager import Screen

# собсна главный скрипт: инициализация окна и вызов команд обновления классов

#---------------------------------------классы и наследование-----------------------------------------------------------

class BaseApp(App):
    def build(self):
        self.canvas = Screen()
        self.background = Widget()
        self.canvas.add_widget(self.background)
        InitRenderer(self.background)
        self.player = Player(self.canvas)
        return self.canvas
    #def update(self, *args):



#-----------------------------------------инициализация окна------------------------------------------------------------

Window.size = (500, 500)
ThisApp = BaseApp()
ThisApp.run()


