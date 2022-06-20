from time import sleep
import random

class apple:
    def __init__(self,pygame,surface,size):
        self.surface = surface
        self.pygame = pygame
        self.size = size
        self.appleObj = pygame.image.load("resource/apple.png").convert_alpha()
        self.appleObj = pygame.transform.scale(self.appleObj, (size, size))
        self.position_x = 280
        self.position_y = 280
        self.draw()

        self.forbiddenArea = []
        self.forbiddenPositions = []

    def getXY(self):
        return [self.position_x,self.position_y]

    def draw(self):
        self.surface.blit(self.appleObj,(self.position_x,self.position_y))

    def eaten(self,width,height,forbidden):
        # print("i have been eaten")
        self.forbiddenPositions = []
        self.forbiddenArea = [width,height]
        for i in range(len(forbidden[0])):
            self.forbiddenPositions.append([forbidden[0][i],forbidden[1][i]])
        
        self.changePosition()

    def changePosition(self):
        AllowedPosition = []
        
        for i in range(10,self.forbiddenArea[0] - 10,30):
            for j in range(10,self.forbiddenArea[1] - 1 - self.size,30):
                if [i,j] not in self.forbiddenPositions:
                    AllowedPosition.append([i,j])

        self.position_x ,self.position_y = random.choice(AllowedPosition)



    def restart(self):
        self.position_x = 280
        self.position_y = 280
        self.draw()
