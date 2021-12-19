import PerlinNoise
import queue
import MapRenderer
from threading import Thread

class Chunk:
    def __init__(self, coord, PNFactory):
        self.minCoord = coord
        self.maxCoord = (coord[0] + 100, coord[1] + 100)
        self.data = [[0 for i in range(100)] for j in range(100)]

        for i in range(100):
            for j in range(100):
                if PNFactory((i + 10000 + coord[0]) / 10, (j + 10000 + coord[1]) / 10) > 0.03:
                    self.data[i][j] = 1
                else:
                    self.data[i][j] = 0
        self.Renderer = MapRenderer.ChunkRenderer(self)

    def Data(self, pos):
        return self.data[pos[0] - self.minCoord[0]][pos[1] - self.minCoord[1]]

    def FreePoint(self, pos):
        self.data[pos[0] - self.minCoord[0]][pos[1] - self.minCoord[1]] = 1
        self.Renderer.RedrawCell(pos)

class BattleMap:
    def __init__(self):
        self.minPos = (25, 25)
        self.maxPos = (75, 75)
        self.PNFactory = PerlinNoise.PerlinNoiseFactory(2, 3, unbias=True)
        self.Chunks = [Chunk((0, 0), self.PNFactory)]


    def GetDistances(self, pos, maxDistance):
        pathMap = [[0 for i in range(maxDistance * 2 + 1)] for j in range(maxDistance * 2 + 1)]
        coordPool = queue.Queue()
        coordPool.put(pos)
        currentChunk = self.__FindChunk__(pos)

        while coordPool.qsize() > 0:
            coord = coordPool.get()

            for x in range(coord[0] - 1, coord[0] + 2):
                for y in range(coord[1] - 1, coord[1] + 2):
                    if pathMap[coord[0] + maxDistance - pos[0]][coord[1] + maxDistance - pos[1]] < maxDistance:
                        if pathMap[x + maxDistance - pos[0]][y + maxDistance - pos[1]] == 0 and \
                                (x != pos[0] or y != pos[1]):

                            areaIsClear = False
                            try:
                                if currentChunk.Data((x, y)) == 1:
                                    areaIsClear = True
                            except IndexError:
                                map = self.__FindChunk__((x, y))
                                if map.Data((x, y)) == 1:
                                    areaIsClear = True

                            if areaIsClear == True:
                                pathMap[x + maxDistance - pos[0]][y + maxDistance - pos[1]] = \
                                    pathMap[coord[0] + maxDistance - pos[0]][coord[1] + maxDistance - pos[1]] + 1
                                coordPool.put((x,y))
                            elif pathMap[coord[0] + maxDistance - pos[0]][coord[1] + maxDistance - pos[1]] == 0:
                                pathMap[x + maxDistance - pos[0]][y + maxDistance - pos[1]] = -1

        return pathMap

    def CheckChunks(self, playerPos):
        if playerPos[0] < self.minPos[0]:
            playerPosY = playerPos[1]
            if playerPosY < 0:
                playerPosY -= 100
            self.Chunks.append(Chunk((self.minPos[0] - 125, (playerPosY // 100)*100), self.PNFactory))
            self.minPos = (self.minPos[0] - 100, self.minPos[1])
        if playerPos[1] < self.minPos[1]:
            playerPosX = playerPos[0]
            if playerPosX < 0:
                playerPosX -= 100
            self.Chunks.append(Chunk(((playerPosX // 100)*100, self.minPos[1] - 125), self.PNFactory))
            self.minPos = (self.minPos[0], self.minPos[1] - 100)
        if playerPos[0] > self.maxPos[0]:
            playerPosY = playerPos[1]
            if playerPosY < 0:
                playerPosY -= 100
            self.Chunks.append(Chunk((self.maxPos[0] + 25, (playerPosY // 100)*100), self.PNFactory))
            self.maxPos = (self.maxPos[0] + 100, self.maxPos[1])
        if playerPos[1] > self.maxPos[1]:
            playerPosX = playerPos[0]
            if playerPosX < 0:
                playerPosX -= 100
            self.Chunks.append(Chunk(((playerPosX // 100)*100, self.maxPos[1] + 25), self.PNFactory))
            self.maxPos = (self.maxPos[0], self.maxPos[1] + 100)

    def ClearCell(self, pos):
        chunk = self.__FindChunk__(pos)
        chunk.FreePoint(pos)

    def __FindChunk__(self, pos):
        for chunk in self.Chunks:
            if pos[0] >= chunk.minCoord[0] and pos[1] >= chunk.minCoord[1] and \
                    pos[0] < chunk.maxCoord[0] and pos[1] < chunk.maxCoord[1]:
                return chunk

        raise ValueError

