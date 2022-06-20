import os
import sys
import pygame
from pygame.locals import *
from pygame import mixer
from time import sleep
# COMPONENTS
from Components.background import background
from Components.dino import dino
from Components.cactus import cactus


class Main:
    def __init__(self):
        self.width = 700
        self.height = 180

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dino Game")
        # background image
        self.gameover = pygame.image.load("resource/gameover_text.png").convert_alpha()
        self.replay = pygame.image.load("resource/replay_button.png").convert_alpha()

        # sound
        self.scoreup = pygame.mixer.Channel(2)
        self.dead = pygame.mixer.Channel(3)
        # self.surface.fill((66, 163, 60))
        self.font = pygame.font.Font("resource/PressStart2P.ttf",13)


        self.background = background(pygame, self.surface)
        self.cactus = cactus(pygame, self.surface)
        self.dino = dino("Dino",pygame, self.surface)

        self.score = 0
        self.Highscore = 0
        self.speed = 3

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
                        else:self.pause = not self.pause
                if event.type == QUIT:
                    os._exit(1)
            

            if self.lost:
                self.surface.blit(self.gameover,(int(self.width / 2) - 98,int(self.height / 2) - 46))
                self.surface.blit(self.replay,(int(self.width / 2) - 17,int(self.height / 2) - 20))
                
                sleep(0.1)
            elif self.pause:
                sleep(0.1)
            else:
                self.handle_keys()
                if self.isDinoBumpedIntoCactus():
                    self.lost = True
                    self.dead.play(pygame.mixer.Sound("resource/dead.wav"))
                    self.dino.killDino()
                    if int(self.score) > self.Highscore:self.Highscore = int(self.score)

                if int(self.score) % 100 == 0 and  int(self.score) != 0:
                    self.scoreup.play(pygame.mixer.Sound("resource/scoreup.wav"))
                    self.speed += 0.01
                elif int(self.score) >= 300:
                    self.cactus.startUseBirds()
                self.score += 0.13 + (self.speed / 100)
                self.fill()
                self.background.walk(self.speed)
                self.cactus.walk(self.speed)
                self.background.draw()
                self.cactus.draw()
                self.dino.draw()
                
                sleep(0.01)
                
                
            pygame.display.flip()
    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # UP
            self.dino.goUp()
        elif key[pygame.K_DOWN]:
            # DOWN
            self.dino.goDown()
            
    def isDinoBumpedIntoCactus(self):
        dinoXY = self.dino.getXY()
        height = 40
        for cactus in self.cactus.getAllXY():
            if dinoXY[1] >= 124:height = 26
            else:height = 40
            if cactus[2] == 104:
                if cactus[1] <= dinoXY[0] + 10 <= cactus[1] + 15 or cactus[1] + 8 <= dinoXY[0] + 40 <= cactus[1] + 15:
                    if cactus[2] <= dinoXY[1] + height <= cactus[2] + 46:
                        return True
            elif cactus[2] == 90:
                if cactus[1] <= dinoXY[0] + 10 <= cactus[1] + 26 or cactus[1] <= dinoXY[0] + 40 <= cactus[1] + 26:
                    if cactus[2] <= dinoXY[1] <= cactus[2] + 20:
                        return True
            else:
                if cactus[1] <= dinoXY[0] + 10 <= cactus[1] + 40 or cactus[1] + 5<= dinoXY[0] + 40 <= cactus[1] + 40:
                    if cactus[2] <= dinoXY[1] + height <= cactus[2] + 33:
                        return True
        return False

    def restart(self):
        self.lost = False
        self.speed = 3
        self.score = 0
        self.dino.restart()
        self.cactus.generateCactus()
        self.background.generateGroundClouds()


    def fill(self):
        self.surface.fill((247, 247, 247))
        StrScore = "0" * (5 - len(str(int(self.score)))) + str(int(self.score))
        HeighScore = "0" * (5 - len(str(self.Highscore))) + str(self.Highscore)
        score = self.font.render(f"HI {HeighScore} {StrScore}",True,(83,83,83))
        self.surface.blit(score,(self.width - 190,10))
        
    

main_game = Main()
main_game.run()
