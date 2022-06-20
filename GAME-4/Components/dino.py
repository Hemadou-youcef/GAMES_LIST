from asyncio.windows_events import NULL
from operator import iand
from time import sleep
import threading
import random


class dino:
    def __init__(self,name, pygame, surface):
        self.name = name
        self.surface = surface
        self.pygame = pygame
    
        
        self.dinoF1 = self.pygame.image.load("resource/main-character1.png").convert_alpha()
        self.dinoF2 = self.pygame.image.load("resource/main-character2.png").convert_alpha()
        self.dinoF3 = self.pygame.image.load("resource/main-character3.png").convert_alpha()
        self.dinoF4 = self.pygame.image.load("resource/main-character4.png").convert_alpha()
        self.dinoF5 = self.pygame.image.load("resource/main-character5.png").convert_alpha()
        self.dinoF6 = self.pygame.image.load("resource/main-character6.png").convert_alpha()

        self.jump = self.pygame.mixer.Channel(1)

        self.position_x = 50
        self.position_y = 107
        
        self.gravity = 0.3
        self.acculurator = 0
        
        self.isDead = False
        self.inAir = False
        self.useOtherFoot = False
        self.isDown = False
        self.JumpThreadWorking = False
        self.DownThreadWorking = False
        self.TestThreadWorking = False

        self.currentFigure = self.dinoF1

        self.downTime = 3
        self.clickedTime = 0
        self.clickedTimeCount = 0
        
        threading.Thread(target=self.currentDinoFigure, args=(),).start()
        # self.draw()

    def getXY(self):
        return [self.position_x, self.position_y]

    def draw(self):
        self.surface.blit(self.currentFigure,(self.position_x,self.position_y))
    
    def goDown(self):
        self.isDown = True
        if self.DownThreadWorking:
            self.downTime = 3
        else:    
            self.DownThreadWorking = True
            self.downTime = 3
            threading.Thread(target=self.stayDownUntilTimeIsUp, args=(),).start()

    def goUp(self):
        if not self.JumpThreadWorking:   
            self.isDown = False
            self.inAir = True
            self.acculurator = 7
            self.TestThreadWorking = False
            self.JumpThreadWorking = True
            threading.Thread(target=self.AccCalcer, args=(),).start()
            # if not self.TestThreadWorking:
            #     self.clickedTime = 3
            #     self.clickedTimeCount = 0
            #     self.TestThreadWorking = True
            #     threading.Thread(target=self.CheckLowMaxJump, args=(),).start()
            # else:
            #     self.clickedTime = 1
            
        self.clickedTimeCount += 1
        # print(self.clickedTimeCount)
      
    def killDino(self):
        self.isDead = True
        self.currentFigure = self.dinoF4
        if self.position_y == 124:self.position_y = 107

    def currentDinoFigure(self):
        while True:
            if self.isDead:
                sleep(0.05)
            elif not self.inAir:
                if self.useOtherFoot:
                    if self.isDown:
                        self.currentFigure = self.dinoF5
                        self.position_y = 124
                    else:
                        self.currentFigure = self.dinoF1
                        self.position_y = 107
                    self.useOtherFoot = False
                else:
                    if self.isDown:
                        self.currentFigure = self.dinoF6
                        self.position_y = 124
                    else:
                        self.currentFigure = self.dinoF2
                        self.position_y = 107
                    self.useOtherFoot = True
                
                sleep(0.05)
            else:
                self.currentFigure = self.dinoF3
                sleep(0.05)

    def CheckLowMaxJump(self):
        while self.clickedTime >= 0 and self.clickedTimeCount <= 15:
            self.clickedTime -= 1
            sleep(0.005)
        print(str(self.clickedTimeCount) + " CHECK")
        if self.clickedTimeCount > 15:self.acculurator = 7
        else:self.acculurator = 6

        self.clickedTime = 0
        self.clickedTimeCount = 0
        

        self.TestThreadWorking = False
        self.JumpThreadWorking = True
        threading.Thread(target=self.AccCalcer, args=(),).start()
        
        

    def AccCalcer(self):
        self.jump.play(self.pygame.mixer.Sound("resource/jump.wav"))
        while self.acculurator >= 0 or (self.position_y < 107 and self.acculurator < 0):
            self.position_y -= self.acculurator
            self.acculurator -= self.gravity
            sleep(0.01)
            
        self.clickedTime = 0
        self.position_y = 107
        self.inAir = False
        self.JumpThreadWorking = False


    def stayDownUntilTimeIsUp(self):
        
        while self.downTime > 0:
            self.downTime -= 1
            sleep(0.01)
        self.isDown = False
        self.DownThreadWorking = False

    def restart(self):
        self.position_x = 50
        self.position_y = 107
        
        self.gravity = 0.3
        self.acculurator = 0
        
        self.isDead = False
        self.inAir = False
        self.useOtherFoot = False
        self.isDown = False
        self.JumpThreadWorking = False
        self.DownThreadWorking = False

        self.currentFigure = self.dinoF1

        self.downTime = 3
        self.clickedTime = 0
        self.draw()
