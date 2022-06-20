from asyncio.windows_events import NULL
from operator import iand
from time import sleep
import threading
import math
from typing import Any


class car:
    def __init__(self,name, pygame, surface):
        self.name = name
        self.surface = surface
        self.pygame = pygame
    
        
        self.car1 = self.pygame.image.load("resource/image/cars/car1.png").convert_alpha()
        self.Origincar1 = self.pygame.transform.scale(self.car1, (28, 13))
        self.car1 = self.pygame.transform.scale(self.car1, (28, 13))
        
        self.currentRotation = 10
        self.rotation = 10


        self.jump = self.pygame.mixer.Channel(1)

        self.position_x = 120
        self.offset_xpos = 120

        self.position_y = 420
        self.offset_ypos = 420

        self.monitor_line_right = Any
        self.monitor_line_left = Any

        self.rotateCar()
        self.draw()

    def getXY(self):
        return [int(self.offset_xpos), int(self.offset_ypos)]

    def getAngle(self):
        return self.currentRotation

    def getCar(self):
        return self.car1

    def getMonitorPoint(self):
        return self.calculateDisplacement(self.position_x,self.position_y,-self.currentRotation,20)

    def draw(self):
        rotate_angle = -self.currentRotation
        monitor_position_source = self.calculateDisplacement(self.position_x,self.position_y,rotate_angle,20)
        monitor_position_right = self.calculateDisplacement(monitor_position_source[0],monitor_position_source[1],rotate_angle + 45,100)
        monitor_position_left = self.calculateDisplacement(monitor_position_source[0],monitor_position_source[1],rotate_angle - 45,100)

        self.monitor_line_left = self.pygame.draw.line(self.surface, (0,0,0), monitor_position_source, monitor_position_left)
        self.monitor_line_right = self.pygame.draw.line(self.surface, (255,0,0), monitor_position_source, monitor_position_right)
        self.surface.blit(self.car1,(self.offset_xpos,self.offset_ypos))

    def rotateLeft(self):
        
        if self.currentRotation == 180 : self.currentRotation = -178
        else: self.currentRotation += 2
        self.rotateCar()
    
    def rotateRight(self):
        if self.currentRotation == -180 : self.currentRotation = 178
        else: self.currentRotation -= 2
        self.rotateCar()

    def goForward(self):
        offset_x, offset_y = self.calculateDisplacement(0,0,self.currentRotation,10)
        self.position_x += offset_x / 5
        self.position_y -= offset_y / 5
        self.rotateCar()

    def calculateDisplacement(self,x,y,angle,length):
        y += math.sin(math.radians(angle)) * length
        x += math.cos(math.radians(angle)) * length
        return x,y
    
    def rotateCar(self):
        x,y = [0,0]
        if 0 <= self.currentRotation <= 90:
            x,y = self.calculateDisplacement(0,0,90 - self.currentRotation,6)
            y += math.cos(math.radians(90 - self.currentRotation)) * 26
        elif -90 <= self.currentRotation < 0 :
            x,y = self.calculateDisplacement(0,0,-1 * self.currentRotation   + 90,6)
            x += math.cos(math.radians(90 + self.currentRotation)) * 13
        elif 90 < self.currentRotation < 180:
            x,y = self.calculateDisplacement(0,0,self.currentRotation % 90,6)
            x += math.sin(math.radians(self.currentRotation % 90)) * 26
            y = math.cos(math.radians(self.currentRotation % 90)) * 26 + math.sin(math.radians(self.currentRotation % 90)) * 13 - y
        elif -180 < self.currentRotation < -90:
            x,y = self.calculateDisplacement(0,0,-1 * self.currentRotation % 90,6)
            x += math.cos(math.radians(self.currentRotation % 90)) * 26
        elif self.currentRotation == 180:
            x = 26
            y = 6
        elif self.currentRotation == -180:
            x = 26
            y = 6

        self.offset_xpos = self.position_x - x
        self.offset_ypos = self.position_y - y
        self.car1 = self.pygame.transform.rotate(self.Origincar1, self.currentRotation)


    def restart(self):
        self.currentRotation = -90
        self.rotation = -90

        self.position_x = 120
        self.offset_xpos = 120

        self.position_y = 420
        self.offset_ypos = 420

        self.rotateCar()
        self.draw()
