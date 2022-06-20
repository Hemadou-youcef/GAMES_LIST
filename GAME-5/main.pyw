import os
import sys
import pygame
from pygame.locals import *
from pygame import mixer
from time import sleep
import math
# COMPONENTS
from Components.map import map
from Components.car import car

class Main:
    def __init__(self):
        self.width = 900
        self.height = 600

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Car Game")

        # sound
        self.scoreup = pygame.mixer.Channel(2)
        self.dead = pygame.mixer.Channel(3)
        # self.surface.fill((66, 163, 60))
        self.font = pygame.font.Font("resource/PressStart2P.ttf",13)


        self.map = map(pygame, self.surface)
        self.car = car("P1",pygame, self.surface)

        self.score = [0]
        self.Highscore = 0

        self.lost = False
        self.pause = False

    def run(self):
        self.running = True

        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == 27:
                        os._exit(1)
                    # elif event.key == K_SPACE:
                    #     self.dino.goUp()
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        if self.lost:self.restart()
                if event.type == QUIT:
                    os._exit(1)
            

            if self.lost:
                result = self.font.render("You lost Press Entre to restart",True,(255,255,255))
                self.surface.blit(result,(int(self.width / 2) - 200,int(self.height / 2) - 50))
                pygame.display.flip()

                sleep(0.1)
            else:
                
                self.fill()
                self.handle_keys()
                self.map.draw()
                self.car.draw()
                if self.isCarsCollision() : self.lost = True
                if self.isCarReachTheLine():
                    self.score[0] += 1
                    self.map.showLine(self.score[0])
                sleep(0.01)
                
                
            pygame.display.flip()
    def handle_keys(self):
        
        key = pygame.key.get_pressed()
        Input = self.calculateLinesCollision()
        if key[pygame.K_SPACE]:
            # UP
            self.dino.goUp()
        elif key[pygame.K_w]:
            # DOWN
            self.car.goForward()
        if key[pygame.K_a]:
            # DOWN
            self.car.rotateLeft()
        elif key[pygame.K_d]:
            # DOWN
            self.car.rotateRight()
    
    def calculateLinesCollision(self):
        Point = self.car.getMonitorPoint()
        Map = self.map.getMap()
        nearestCollision = [100,100]

        for i in range(100):
            position_right = self.calculateDisplacement(Point[0],Point[1],self.car.getAngle() + 45,i)
            position_left = self.calculateDisplacement(Point[0],Point[1],self.car.getAngle() - 45,i)
            if nearestCollision[1] == 100:
                if  Map.get_at(position_right).a != 0:
                    nearestCollision[1] = i

            if nearestCollision[0] == 100:
                if  Map.get_at(position_left).a != 0:
                    nearestCollision[0] = i
        return nearestCollision

    def calculateDisplacement(self,x,y,angle,length):
        x = x + length * math.cos(math.radians(angle))
        y = y - length * math.sin(math.radians(angle))
        return int(x),int(y)

    def isCarReachTheLine(self):
        Line = self.map.getLine()
        Car = self.car.getCar()
        carXY = self.car.getXY()
        for i in range(28):
            for j in range(28):
                try:
                    if Car.get_at((i,j)).a != 0:
                        if  Line.get_at((carXY[0] + i,carXY[1] + j)).a != 0:
                            return True
                except:
                    pass
        return False

    def isCarsCollision(self):
        Map = self.map.getMap()
        Car = self.car.getCar()
        carXY = self.car.getXY()
        for i in range(28):
            for j in range(28):
                try:
                    if Car.get_at((i,j)).a != 0:
                        if  Map.get_at((carXY[0] + i,carXY[1] + j)).a != 0:
                            return True
                except:
                    pass
        return False

    def restart(self):
        self.lost = False
        self.map.generateRandomMap()
        self.car.restart()


    def fill(self):
        self.surface.fill((17, 39, 54))
    
    

main_game = Main()
main_game.run()
