from cProfile import run
from curses.ascii import ESC
from json.encoder import ESCAPE
import pygame
from pygame.locals import *
from time import sleep

def draw_background():
    surface.fill((66, 163, 60))
    pygame.display.flip()
    
def draw_block():
    surface.blit(block,(block_x,block_y))
    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((500,400))
    pygame.display.set_caption("My Game")
    surface.fill((66, 163, 60))

    #IMAGES
    block = pygame.image.load("resource/block.png").convert_alpha()
    block = pygame. transform. scale(block, (50, 50))

    block_x = 10
    block_y = 10
    surface.blit(block,(block_x,block_y))


    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    block_y = block_y - 10
                    draw_background()
                    draw_block()
                elif event.key == K_DOWN:
                    block_y = block_y + 10
                    draw_background()
                    draw_block()
                elif event.key == K_LEFT:
                    block_x = block_x - 10
                    draw_background()
                    draw_block()
                elif event.key == K_RIGHT:
                    block_x = block_x + 10
                    draw_background()
                    draw_block()
                
                
                print(event.key)
            elif event.type == QUIT:
                running = False

def move_block(x,y,type):
    if type == 0:
        y = y - 10
    elif type == 1:
        x = x + 10
    elif type == 2:
        y = y + 10
    elif type == 3:
        x = x - 10   

    return [x,y]