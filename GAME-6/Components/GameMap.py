from time import sleep
import random

class GameMap:
    def __init__(self,pygame,surface,width,height):
        self.surface = surface
        self.pygame = pygame
        self.width = width
        self.height = height

        # IMAGE
        self.map = any
        self.generateRandomMap()
        self.draw()

    def generateRandomMap(self):
        self.map = self.pygame.image.load("resource/image/maps/forest.jpg").convert_alpha()
        self.map = self.pygame.transform.scale(self.map, (self.width, self.height))
        
    def draw(self):
        self.surface.blit(self.map,(0,0))

        


