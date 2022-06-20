from time import sleep
import random
import threading

class cactus:
    def __init__(self,pygame,surface):
        self.surface = surface
        self.pygame = pygame

        # Persontage
        self.Gdcactus = 0.3
        self.Gnbird = 0.5

        # config
        # self.CactusHeight = 104

        # IMAGE
        self.cactus1 = pygame.image.load("resource/cactus1.png").convert_alpha()
        self.cactus2 = pygame.image.load("resource/cactus2.png").convert_alpha()
        self.bird1 = pygame.image.load("resource/bird1.png").convert_alpha()
        self.bird2 = pygame.image.load("resource/bird2.png").convert_alpha()

        self.cactus = []
        self.currentBird = self.bird1

        self.useOtherWing = False
        self.startUsingBirds = False
        self.generateCactus()
        threading.Thread(target=self.birdFly, args=(),).start()
        self.draw()
    

    def getAllXY(self):
        return self.cactus

    def draw(self):
        for obstacle in self.cactus:
            if obstacle[2] == 90: self.surface.blit(self.currentBird,(obstacle[1],obstacle[2]))
            else: self.surface.blit(obstacle[0],(obstacle[1],obstacle[2]))

    def startUseBirds(self):
        self.startUsingBirds = True

    def generateCactus(self):
        self.startUsingBirds = False
        self.cactus = []
        X_width = 1200
        for i in range(10):
            prob = random.uniform(0,1)
            if prob < self.Gdcactus:
                self.cactus.append([self.cactus2,X_width,117])
            elif prob < self.Gnbird and self.startUsingBirds:
                self.cactus.append([self.bird1,X_width,90])
            else:
                self.cactus.append([self.cactus1,X_width,104])
            X_width += random.randint(200,500)

    def walk(self,speed):
        for Index,obstacle in enumerate(self.cactus):
            obstacle[1] -= speed
            if obstacle[1] + 71 <= 0:
                self.cactus.pop(Index)

                X_width = self.cactus[len(self.cactus) - 1][1] + random.randint(200,500)
                prob = random.uniform(0,1)
                if prob < self.Gdcactus:
                    self.cactus.append([self.cactus2,X_width,117])
                elif prob < self.Gnbird and self.startUsingBirds:
                    self.cactus.append([self.bird1,X_width,90])
                else:
                    self.cactus.append([self.cactus1,X_width,104])
    
    def birdFly(self):
        while True:
            if self.useOtherWing : self.currentBird = self.bird1
            else: self.currentBird = self.bird2
            self.useOtherWing = not self.useOtherWing
            sleep(0.2)

        


