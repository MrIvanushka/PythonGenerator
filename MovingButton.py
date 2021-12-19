from kivy.uix.button import Button
from kivy.uix.image import Image

class MovingButton(Button):
    def __init__(self, pos, distance, player):
        Button.__init__(self)
        self.GFX = Image()
        self.add_widget(self.GFX)
        self.GFX.color = (1, 0, 0)
        self.background_color = (0, 0, 0, 0)
        self.GFX.size = self.size = (8, 8)
        self.pos = self.GFX.pos = (pos[0]*10, pos[1] * 10)
        self.bind(on_press = lambda x: player.Move(pos, distance))