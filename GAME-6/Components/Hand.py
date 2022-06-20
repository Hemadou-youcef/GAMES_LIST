from time import sleep
import threading


class Hand:
    def __init__(self,pygame, surface,width,height):
        self.surface = surface
        self.pygame = pygame
        self.width = width
        self.height = height
        
        self.hand = self.pygame.image.load("resource/image/hand/normal_hand.png").convert_alpha()
        self.hand = self.pygame.transform.scale(self.hand, (60, 120))

        self.position_x = int(width / 2)
        self.position_y = int(height / 2)

        self.attackThread = False

        self.draw()

    def getXY(self):
        return [int(self.position_x), int(self.position_y)]

    def setXY(self,x,y):
        self.position_x = x
        self.position_y = y

    def draw(self):
        self.surface.blit(self.hand, (self.position_x,self.position_y))

    def attack(self):
        if self.attackThread == False:
            self.attackThread = True
            threading.Thread(target=self.attackThreadFunction).start()
    
    def attackThreadFunction(self):
        self.hand = self.pygame.image.load("resource/image/hand/attack_hand.png").convert_alpha()
        self.hand = self.pygame.transform.scale(self.hand, (60, 120))
        sleep(0.5)
        self.hand = self.pygame.image.load("resource/image/hand/normal_hand.png").convert_alpha()
        self.hand = self.pygame.transform.scale(self.hand, (60, 120))
        self.attackThread = False

    def restart(self):
        self.position_x = 0
        self.position_y = 0
        self.draw()
