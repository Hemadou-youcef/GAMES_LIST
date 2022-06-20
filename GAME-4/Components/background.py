from time import sleep
import random

class background:
    def __init__(self,pygame,surface):
        self.surface = surface
        self.pygame = pygame

        # Persontage
        self.Gobs = 0.1
        self.Gobs2 = 0.2
        self.Scl = 0.3

        # config
        self.GroundHeight = 130
        self.MinCloudHeight = 30
        self.MaxCloudHeight = 110

        # IMAGE
        self.land1 = pygame.image.load("resource/land1.png").convert_alpha()
        self.land2 = pygame.image.load("resource/land2.png").convert_alpha()
        self.land3 = pygame.image.load("resource/land3.png").convert_alpha()

        self.cloud = pygame.image.load("resource/cloud.png").convert_alpha()

        self.ground = []
        self.clouds = []
        self.generateGroundClouds()
        
        self.draw()
    

    def draw(self):
        for block in self.ground:
            self.surface.blit(block[0],(block[1],self.GroundHeight))

        for cloud in self.clouds:
            self.surface.blit(self.cloud,(cloud[0],cloud[1]))

    def generateGroundClouds(self):
        self.ground = []
        self.clouds = []
        X_width = 0
        for i in range(50):
            prob = random.uniform(0,1)
            if prob < self.Gobs:
                self.ground.append([self.land1,X_width])
            elif prob < self.Gobs2:
                self.ground.append([self.land3,X_width])
            else:
                self.ground.append([self.land2,X_width])

            if prob < self.Scl:
                height = random.randint(self.MinCloudHeight,self.MaxCloudHeight)
                self.clouds.append([X_width,height])
            X_width += 71
    
    def walk(self,speed):
        for Index,block in enumerate(self.ground):
            block[1] -= speed
            if block[1] + 71 <= 0:
                self.ground.pop(Index)

                X_width = self.ground[len(self.ground) - 1][1] + 71
                prob = random.uniform(0,1)
                if prob < self.Gobs:
                    self.ground.append([self.land1,X_width])
                elif prob < self.Gobs2:
                    self.ground.append([self.land3,X_width])
                else:
                    self.ground.append([self.land2,X_width])
        for Index,cloud in enumerate(self.clouds):
            cloud[0] -= speed
            if cloud[0] + 71 <= 0:
                self.clouds.pop(Index)
                X_width = self.clouds[len(self.clouds) - 1][0] + 71
                while True:
                    prob = random.uniform(0,1)
                    if prob < self.Scl:
                        height = random.randint(self.MinCloudHeight,self.MaxCloudHeight)
                        self.clouds.append([X_width,height])
                        break
                    X_width += 71

        


