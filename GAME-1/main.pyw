from os import environ
import pygame
from pygame.locals import *
from pygame import mixer
from time import sleep
# COMPONENTS
from Components.snake import snake
from Components.apple import apple


class Main:
    def __init__(self):
        self.width = 620
        self.height = 620
        self.size = 30

        pygame.init()
        self.surface = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Snake Game")

        #background image
        self.background = pygame.image.load("resource/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.surface.blit(self.background,(0,0))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(0, 0, self.width, self.height),  10)

        #sound
        self.background_sound = mixer.Channel(0)
        self.background_sound.play(mixer.Sound("resource/background.mp3"),-1)
        
        self.eating_sound = mixer.Channel(1)
       

        # self.surface.fill((66, 163, 60))
        
        self.Main_snake = snake(pygame,self.surface,self.size)
        self.Main_apple = apple(pygame,self.surface,self.size)

        self.score = 0
        self.stopPlaying = False
        self.lost = False
    def run(self):
        self.running = True

        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == 27:
                        self.running = False
                    elif event.key == K_UP:
                        # UP
                        self.Main_snake.setDirection("up")
                    elif event.key == K_DOWN:
                        # DOWN
                        self.Main_snake.setDirection("down")
                    elif event.key == K_LEFT:
                        # LEFT
                        self.Main_snake.setDirection("left")
                    elif event.key == K_RIGHT:
                        # RIGHT
                        self.Main_snake.setDirection("right")
                    elif event.key == K_RETURN or event.key == K_KP_ENTER:
                        # RESTART
                        self.restart()
                    # print(event.key)
                elif event.type == QUIT:
                    self.running = False

            if not self.stopPlaying:
                self.fill()

                self.Main_apple.draw()

                if self.didSnakePassTheLimit(self.Main_snake.nextPosition()):
                    self.Lost()
                    continue

                self.Main_snake.walk()

                if self.didSnakeEatApple():self.Eaten()
                if self.didSnakeEatHisTail():self.Lost()
                sleep(0.1)
            elif self.lost:
                self.surface.fill((66, 163, 60))
                font = pygame.font.SysFont("Calibri",30)
                score = font.render("You lost :( Press Entre to restart",True,(255,255,255))
                self.surface.blit(score,(int(self.width / 2) - 200,int(self.height / 2) - 50))
                pygame.display.flip()
                sleep(0.5)
            else:
                sleep(0.5)
    
    def restart(self):
        # print("restart")
        self.fill()
        self.stopPlaying = False
        self.lost = False
        self.score = 0
        self.Main_snake.restart()
        self.Main_apple.restart()

    def Eaten(self):
        self.Main_snake.get_bigger()
        self.Main_apple.eaten(self.width,self.height,self.Main_snake.getAllXY())
        self.score += 10
        self.eating_sound.play(mixer.Sound("resource/Crunch.mp3"))

    def Lost(self):
        self.stopPlaying = True
        self.lost = True
        # print("You Lost")

    def didSnakeEatApple(self):
        snakeXY = self.Main_snake.getXY()
        appleXY = self.Main_apple.getXY()

        if snakeXY[0] == appleXY[0] and snakeXY[1] == appleXY[1]:
            return True
        return False

    def didSnakeEatHisTail(self):
        snakeAllXY = self.Main_snake.getAllXY()
        for i in range(1,len(snakeAllXY[0])):
            if snakeAllXY[0][0] == snakeAllXY[0][i] and snakeAllXY[1][0] == snakeAllXY[1][i]:
                return True
        return False

    def didSnakePassTheLimit(self,pos):
        snakeXY = pos
        print(snakeXY)
        if 10 <= snakeXY[0] <= self.width - 10 - self.size and 10 <= snakeXY[1] <= self.height - 10 - self.size :
            return False
        return True

    def displayScore(self):
        font = pygame.font.SysFont("Calibri",30)
        score = font.render(f"Score:{self.score}",True,(255,255,255))
        self.surface.blit(score,(self.width - 120,10))

    def fill(self):
        self.surface.blit(self.background,(0,0))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(0, 0, self.width, self.height),  10)
        self.displayScore()
        # self.surface.fill((66, 163, 60))

main_game = Main()
main_game.run()