from kivy.uix.button import Button
from kivy.uix.image import Image
from MovingButton import MovingButton
from DiggingButton import DiggingButton
import MapMath
from threading import Thread

class Player(Button):
    def __init__(self, canvas):
        Button.__init__(self)
        self.movingRadius = 3
        self.size = (10, 10)
        self.background_color = (1, 1, 1, 0)
        self.GFX = Image()
        self.GFX.color = (0, 1, 0)
        self.GFX.size = (10, 10)
        self.pos = self.GFX.pos = (500, 500)
        self.add_widget(self.GFX)
        self.bind(on_press=lambda x: self.__OnPress__())
        self.position = (50, 50)
        canvas.pos = (-250, -250)
        canvas.add_widget(self)
        self.movingButtons = []
        self.canvas = canvas
        self.Map = MapMath.BattleMap()

    def __OnPress__(self):
        self.__ShowMoveButtons__()

    def __ShowMoveButtons__(self):
        pathMap = self.Map.GetDistances(self.position, self.movingRadius)
        self.__closeMovingButtons__()

        for x in range(self.position[0] - self.movingRadius, self.position[0] + self.movingRadius + 1):
            for y in range(self.position[1] - self.movingRadius, self.position[1] + self.movingRadius + 1):
                if (x != self.position[0] or y != self.position[1]) and\
                        pathMap[x+self.movingRadius-self.position[0]][y+self.movingRadius-self.position[1]] > 0:
                    self.movingButtons.append(MovingButton((x,y), pathMap[x+self.movingRadius-self.position[0]][y+self.movingRadius-self.position[1]], self))
                    self.GFX.add_widget(self.movingButtons[len(self.movingButtons) - 1])
                elif pathMap[x+self.movingRadius-self.position[0]][y+self.movingRadius-self.position[1]] < 0:
                    self.movingButtons.append(DiggingButton((x, y), pathMap[x + self.movingRadius - self.position[0]][
                        y + self.movingRadius - self.position[1]], self))
                    self.GFX.add_widget(self.movingButtons[len(self.movingButtons) - 1])

    def Move(self, newPos, distance):
        self.position = newPos
        deltaPos = (newPos[0]*10 - self.pos[0], newPos[1]*10 - self.pos[1])
        self.pos = self.GFX.pos = (newPos[0]*10, newPos[1]*10)
        self.__closeMovingButtons__()
        self.canvas.pos = (self.canvas.pos[0] - deltaPos[0], self.canvas.pos[1] - deltaPos[1])
        self.Map.CheckChunks(self.position)

    def Dig(self, pos):
        self.Map.ClearCell(pos)
        self.__closeMovingButtons__()

    def __closeMovingButtons__(self):
        for button in self.movingButtons:
            self.GFX.remove_widget(button)

        self.movingButtons = []





