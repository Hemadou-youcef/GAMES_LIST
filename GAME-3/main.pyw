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
        self.width = 1010
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
        try:
            self.background_sound = mixer.Channel(0)
            self.background_sound.play(mixer.Sound("resource/background.mp3"),-1)
        except:
            pass
        try:
            self.eating_sound = mixer.Channel(1)
        except:
            pass
        
       

        # self.surface.fill((66, 163, 60))
        
        self.firstSnake = snake("P1",pygame,self.surface,self.width,self.height,self.size,"p1.png",[10 + self.size,10],[10,10])
        self.secondSnake = snake("P2",pygame,self.surface,self.width,self.height,self.size,"p2.png",[self.width - 10 - 2 * self.size,self.width - 10 - self.size],[self.height - 10 - self.size,self.height - 10 - self.size])

        self.Main_apple = apple(pygame,self.surface,self.size)

        self.winner = ""
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
                        self.secondSnake.setDirection("up")
                    elif event.key == K_DOWN:
                        # DOWN
                        self.secondSnake.setDirection("down")
                    elif event.key == K_LEFT:
                        # LEFT
                        self.secondSnake.setDirection("left")
                    elif event.key == K_RIGHT:
                        # RIGHT
                        self.secondSnake.setDirection("right")

                    if event.key == K_w:
                        # UP
                        self.firstSnake.setDirection("up")
                    elif event.key == K_s:
                        # DOWN
                        self.firstSnake.setDirection("down")
                    elif event.key == K_a:
                        # LEFT
                        self.firstSnake.setDirection("left")
                    elif event.key == K_d:
                        # RIGHT
                        self.firstSnake.setDirection("right")

                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        # RESTART
                        self.restart()
                    # print(event.key)
                elif event.type == QUIT:
                    self.running = False

            if not self.stopPlaying:
                self.fill()

                self.Main_apple.draw()

                # if self.didSnakePassTheLimit(self.firstSnake.nextPosition()):
                #     self.Lost("P2")
                #     continue
                # if self.didSnakePassTheLimit(self.secondSnake.nextPosition()):
                #     self.Lost("P1")
                #     continue

                self.firstSnake.walk()
                self.secondSnake.walk()

                if self.firstSnake.getAllXY()[0][0] == self.secondSnake.getAllXY()[0][0] and self.firstSnake.getAllXY()[1][0] == self.secondSnake.getAllXY()[1][0]:
                    self.Lost("TIE")

                if self.didSnakeEatApple(self.firstSnake):self.Eaten(self.firstSnake)
                if self.didSnakeEatApple(self.secondSnake):self.Eaten(self.secondSnake)

                if self.didSnakeEatTail(self.firstSnake,self.secondSnake):self.Lost("P2 win")
                if self.didSnakeEatTail(self.secondSnake,self.firstSnake):self.Lost("P1 win")
                sleep(0.1)
            elif self.lost:
                self.surface.fill((66, 163, 60))
                font = pygame.font.SysFont("Calibri",30)
                
                result = font.render(f"{self.winner} Press Entre to restart",True,(255,255,255))
                self.surface.blit(result,(int(self.width / 2) - 200,int(self.height / 2) - 50))
                pygame.display.flip()
                sleep(0.5)
            else:
                sleep(0.5)
    
    def restart(self):
        # print("restart")
        self.fill()
        self.stopPlaying = False
        self.lost = False
        self.winner = ""
        self.firstSnake.restart([10 + self.size,10],[10,10])
        self.secondSnake.restart([self.width - 10 - 2 * self.size,self.width - 10 - self.size],[self.height - 10 - self.size,self.height - 10 - self.size])
        self.Main_apple.restart()

    def Eaten(self,snake):
        snake.get_bigger()

        allForbiddenAria = [self.firstSnake.getAllXY()[0] + self.secondSnake.getAllXY()[0] ,self.firstSnake.getAllXY()[1]  + self.secondSnake.getAllXY()[1]]
        self.Main_apple.eaten(self.width,self.height,allForbiddenAria)
        try:
            self.eating_sound.play(mixer.Sound("resource/Crunch.mp3"))
        except:
            pass
        

    def Lost(self,winner):
        self.stopPlaying = True
        self.lost = True
        self.winner = winner
        # print("You Lost")

    def didSnakeEatApple(self,snake):
        snakeXY = snake.getXY()
        appleXY = self.Main_apple.getXY()

        if snakeXY[0] == appleXY[0] and snakeXY[1] == appleXY[1]:
            return True
        return False

    def didSnakeEatTail(self,snake,otherSnake):
        snakeAllXY = snake.getAllXY()
        otherSnakeAllXY = otherSnake.getAllXY()
        # for i in range(1,len(snakeAllXY[0])):
        #     if snakeAllXY[0][0] == snakeAllXY[0][i] and snakeAllXY[1][0] == snakeAllXY[1][i]:
        #         return True
        for i in range(1,len(otherSnakeAllXY[0])):
            if snakeAllXY[0][0] == otherSnakeAllXY[0][i] and snakeAllXY[1][0] == otherSnakeAllXY[1][i]:
                return True
        return False

    def didSnakePassTheLimit(self,pos):
        snakeXY = pos
        # print(snakeXY)
        if 10 <= snakeXY[0] <= self.width - 10 - self.size and 10 <= snakeXY[1] <= self.height - 10 - self.size :
            return False
        return True


    def fill(self):
        self.surface.blit(self.background,(0,0))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(0, 0, self.width, self.height),  10)
        # self.surface.fill((66, 163, 60))

main_game = Main()
main_game.run()