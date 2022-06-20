import pygame
from time import sleep

class snake:
    def __init__(self,name,pygame,surface,width,height,size,img,x,y):
        self.surface = surface
        self.pygame = pygame
        self.size = size
        self.width = width
        self.height= height
        self.name = name
        self.snakeObj = pygame.image.load("resource/" + img).convert_alpha()
        self.snakeObj = pygame.transform.scale(self.snakeObj, (size, size))
        self.AllXPosition = x
        self.AllYPosition = y
        self.Direction = "stop"
        self.font = pygame.font.SysFont("Calibri",15, bold=True)
        self.draw()

        self.commanded = False

    def getXY(self):
        return [self.AllXPosition[0],self.AllYPosition[0]]

    def getAllXY(self):
        return [self.AllXPosition,self.AllYPosition]
        
    def draw(self):
        
        for i in range(1,len(self.AllXPosition)):
            self.surface.blit(self.snakeObj,(self.AllXPosition[i],self.AllYPosition[i]))
        self.surface.blit(self.snakeObj,(self.AllXPosition[0],self.AllYPosition[0]))
        
        result = self.font.render(self.name,True,(0,0,0))
        self.surface.blit(result,(self.AllXPosition[0] + int(self.size / 4),self.AllYPosition[0] + int(self.size / 4)))

        self.commanded = False
        self.pygame.display.flip()

    def walk(self):
        move = True
        prevPosition = [self.AllXPosition[0],self.AllYPosition[0]]
        match self.Direction:
            case 'left':
                if self.AllXPosition[0] > 10:
                    self.AllXPosition[0] -= self.size
                elif self.AllXPosition[0] == 10:
                        self.AllXPosition[0] = self.width - 10 - self.size
                    
            case 'right':
                if self.AllXPosition[0] < self.width - self.size - 10:
                    self.AllXPosition[0] += self.size
                elif self.AllXPosition[0] == self.width - self.size - 10:
                    self.AllXPosition[0] = 10
                
            case 'up':
                if self.AllYPosition[0] > 10:
                    self.AllYPosition[0] -= self.size
                elif self.AllYPosition[0] == 10:
                        self.AllYPosition[0] = self.height - 10 - self.size
                 
            case 'down':
                if self.AllYPosition[0] < self.height - self.size - 10:
                    self.AllYPosition[0] += self.size
                elif self.AllYPosition[0] == self.height - self.size - 10:
                    self.AllYPosition[0] = 10
                
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
            self.Direction = direction
            self.commanded = True
        elif self.Direction != direction and not self.commanded:
            if self.Direction in ["right","left"] and direction not in ["right","left"]:
                self.Direction = direction
                self.commanded = True
            elif self.Direction in ["up","down"] and direction not in ["up","down"]:
                self.Direction = direction
                self.commanded = True
        
    
    def restart(self,x,y):
        self.AllXPosition = x
        self.AllYPosition = y
        self.Direction = "stop"
        self.draw()
