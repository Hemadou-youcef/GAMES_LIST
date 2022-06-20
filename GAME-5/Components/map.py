from time import sleep
import random

class map:
    def __init__(self,pygame,surface):
        self.surface = surface
        self.pygame = pygame

        # IMAGE
        self.map = any
        self.line = any
        self.generateRandomMap()
        self.draw()
    
    def getMap(self):
        return self.map
    
    def getLine(self):
        return self.line
    
    def showLine(self,number):
        number = (number % 31) + 1
        self.line = self.pygame.image.load("resource/image/maps/lines2/" + str(number) + ".png").convert_alpha()

    def generateRandomMap(self):

        self.line = self.pygame.image.load("resource/image/maps/lines2/1.png").convert_alpha()
        self.map = self.pygame.image.load("resource/image/maps/map" + str(random.randint(1,3)) + ".png").convert_alpha()

    def draw(self):
        self.surface.blit(self.line,(0,0))
        self.surface.blit(self.map,(0,0))

        


