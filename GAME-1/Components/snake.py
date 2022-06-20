import pygame
from time import sleep

class snake:
    def __init__(self,pygame,surface,size):
        self.surface = surface
        self.pygame = pygame
        self.size = size
        self.snakeObj = pygame.image.load("resource/block.png").convert_alpha()
        self.snakeObj = pygame.transform.scale(self.snakeObj, (size, size))
        self.AllXPosition = [10 + self.size,10]
        self.AllYPosition = [10,10]
        self.Direction = "stop"

        self.draw()

        self.commanded = False

    def getXY(self):
        return [self.AllXPosition[0],self.AllYPosition[0]]

    def getAllXY(self):
        return [self.AllXPosition,self.AllYPosition]
        
    def draw(self):
        for i in range(len(self.AllXPosition)):
            self.surface.blit(self.snakeObj,(self.AllXPosition[i],self.AllYPosition[i]))
        self.commanded = False
        self.pygame.display.flip()

    def walk(self):
        move = True
        prevPosition = [self.AllXPosition[0],self.AllYPosition[0]]
        match self.Direction:
            case 'left':
                self.AllXPosition[0] -= self.size
            case 'right':
                self.AllXPosition[0] += self.size
            case 'up':
                self.AllYPosition[0] -= self.size
            case 'down':
                self.AllYPosition[0] += self.size
            case _:
                move = False
        if move:
            for i in range(1,len(self.AllXPosition)):
                temp_position = [self.AllXPosition[i],self.AllYPosition[i]]
                self.AllXPosition[i] = prevPosition[0]
                self.AllYPosition[i] = prevPosition[1]
                prevPosition = [temp_position[0],temp_position[1]]
                pass

        # print("[X: " + str(self.AllXPosition[0]) + " |Y: " + str(self.AllYPosition[0]) + "]")
        self.draw()

    def nextPosition(self):
        FakeX = self.AllXPosition[0]
        FakeY = self.AllYPosition[0]
        match self.Direction:
            case 'left':
                FakeX -= self.size
            case 'right':
                FakeX += self.size
            case 'up':
                FakeY -= self.size
            case 'down':
                FakeY += self.size
        return [FakeX,FakeY]


    def get_bigger(self):
        self.AllXPosition.append(0)
        self.AllYPosition.append(0)
    def setDirection(self,direction):

        if self.Direction == "stop" and not self.commanded:
            if direction not in ["top","left"]:
                self.Direction = direction
                self.commanded = True
        elif self.Direction != direction and not self.commanded:
            if self.Direction in ["right","left"] and direction not in ["right","left"]:
                self.Direction = direction
                self.commanded = True
            elif self.Direction in ["up","down"] and direction not in ["up","down"]:
                self.Direction = direction
                self.commanded = True
        
    
    def restart(self):
        self.AllXPosition = [10 + self.size,10]
        self.AllYPosition = [10,10]
        self.Direction = "stop"
        self.draw()
