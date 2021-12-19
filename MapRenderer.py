from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

def InitRenderer(canvas):
    global mainCanvas
    mainCanvas = canvas

class ChunkRenderer:
    def __init__(self, map):
        self.RenderMap(map)

    def RenderMap(self, map):
        self.background = Image()
        self.background.color = (0, 0, 0)
        self.background.pos = (map.minCoord[0], map.minCoord[1]);
        mainCanvas.add_widget(self.background)

        for j in range(len(map.data)):
            for i in range(len(map.data[j])):
                WhiteImage = Image()
                WhiteImage.size = (10, 10)
                #WhiteImage.color = (map[i][j], map[i][j], map[i][j])
                if map.data[i][j] == 1:
                    WhiteImage.color = (1, 1, 1)
                    WhiteImage.pos = (10 * (i + map.minCoord[0]), 10 * (j + map.minCoord[1]))
                    self.background.add_widget(WhiteImage)

    def RedrawCell(self, pos):
        WhiteImage = Image()
        WhiteImage.size = (10, 10)
        WhiteImage.color = (1, 1, 1)
        WhiteImage.pos = (10 * pos[0], 10 * pos[1])
        self.background.add_widget(WhiteImage)

mainCanvas = Screen()