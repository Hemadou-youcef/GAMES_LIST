import os
import sys
import pygame
from pygame.locals import *
from pygame import mixer
from time import sleep
import math
import mediapipe as mp
import cv2
# COMPONENTS
from Components.GameMap import GameMap
from Components.Mosquito import Mosquito
from Components.Hand import Hand

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

        self.NumberOfMosquito = 10
        
        self.GameMap = GameMap(pygame, self.surface, self.width, self.height)
        self.Mosquito = Mosquito(pygame, self.surface, self.width, self.height,self.NumberOfMosquito)
        self.Hand = Hand(pygame, self.surface, self.width, self.height)

        self.score = [0]
        self.Highscore = 0

        self.lost = False
        self.pause = False

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        self.tipIds=[4,8,12,16,20]
        self.cap = cv2.VideoCapture(0)

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
                with self.mp_hands.Hands(
                    model_complexity=0,
                    max_num_hands=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
                    if self.cap.isOpened():
                        success, image = self.cap.read()
                        if success:
                            image.flags.writeable = False
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            results = hands.process(image)

                            image.flags.writeable = True
                            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            lmList=[]
                            HandPos = []
                            if results.multi_hand_landmarks:
                                for hand_landmarks in results.multi_hand_landmarks:
                                    myHands=results.multi_hand_landmarks[0]
                                    for id, lm in enumerate(myHands.landmark):
                                        h,w,c=image.shape
                                        cx,cy= int(lm.x*w), int(lm.y*h)
                                        lmList.append([id,cx,cy])
                                        if id == 9:
                                            HandPos = [self.width - lm.x * self.width,lm.y * self.height]
                                    self.mp_drawing.draw_landmarks(
                                        image,
                                        hand_landmarks,
                                        self.mp_hands.HAND_CONNECTIONS,
                                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                        self.mp_drawing_styles.get_default_hand_connections_style())
                            fingers=[]
                            if len(lmList)!=0:
                                if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
                                    fingers.append(1)
                                else:
                                    fingers.append(0)
                                for id in range(1,5):
                                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-2][2]:
                                        fingers.append(1)
                                    else:
                                        fingers.append(0)
                                total=fingers.count(1)

                                if total == 5:
                                    image = cv2.rectangle(image, (10,10), (350,50), (89,61,42), -1)
                                    image = cv2.putText(image, "outstretched hands", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                                if total == 0:
                                    image = cv2.rectangle(image, (10,10), (350,50), (89,61,42), -1)
                                    image = cv2.putText(image, "ATTACK", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                if len(lmList)!=0:
                    self.Hand.setXY(HandPos[0],HandPos[1])
                    if total == 0:
                        self.Hand.attack()
                        HandXY = self.Hand.getXY()
                        for index,Mosquito in enumerate(self.Mosquito.getXY()):
                            if self.isThereAMosquito(Mosquito[0],Mosquito[1],HandXY[0],HandXY[1]):
                                self.score[0] += 1
                                self.Mosquito.killMosquito(index)
                cv2.imshow('MediaPipe Hands',image)
                

                self.GameMap.draw()
                self.Mosquito.draw()
                self.Hand.draw()

                sleep(0.01)
                
                
            pygame.display.flip()

    def isThereAMosquito(self,Mx,My,x,y):
        if x < Mx < x + 60 and y < My < y + 120:
            return True
        return False

    def restart(self):
        self.lost = False
        self.GameMap.generateRandomMap()


    def fill(self):
        self.surface.fill((17, 39, 54))
    
    

main_game = Main()
main_game.run()
