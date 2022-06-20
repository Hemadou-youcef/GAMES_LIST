from time import sleep
import random


class Mosquito:
    def __init__(self,pygame, surface,width,height,number=10):
        self.surface = surface
        self.pygame = pygame
        self.width = width
        self.height = height
        
        self.mosquito = self.pygame.image.load("resource/image/mosquito/mosquito1.png").convert_alpha()
        self.mosquito = self.pygame.transform.scale(self.mosquito, (30, 30))

        self.position_xy = []
        self.generateMosquito(number)
        self.draw()

    def getXY(self):
        return self.position_xy


    def draw(self):
        self.moveAllMosquito()

        for i in range(len(self.position_xy)):
            if self.CheckIfMosquitoIsOutOfScreen(i):
                self.killMosquito(i)
                self.addMosquito()

        for pos in self.position_xy:
            self.surface.blit(self.mosquito, pos)

    #generate random position for mosquito
    def generateMosquito(self,number=10):
        self.position_xy = []
        for i in range(number):
            self.position_xy.append([random.randint(0, self.width), random.randint(0, self.height)])

    def addMosquito(self):
        position_x = random.randint(0, self.width)
        position_y = random.randint(0, self.height)

        self.position_xy.append([position_x,position_y])

    def killMosquito(self,index):
        self.position_xy.pop(index)

    def CheckIfMosquitoIsOutOfScreen(self,index):
        if self.position_xy[index][0] < 0 or self.position_xy[index][0] > self.width:
            return True

    def moveAllMosquito(self):
        for pos in self.position_xy:
            offsetX = random.choice([-1, 0, 1])
            offsetY = random.choice([-1, 0, 1])
            pos[0] += offsetX
            pos[1] += offsetY

    def restart(self):
        self.position_xy = []
        self.generateMosquito()
        self.draw()
