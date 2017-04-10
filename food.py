import copy, pygame, random
from constants import *

class Food:
    def __init__(self, X, Y, SCREEN):
        self.x = X
        self.y = Y
        self.screen = SCREEN
    def getNew(self, use):
        self.x = random.randint(0, W - 1)
        self.y = random.randint(0, H - 1)
        while [self.x, self.y] in use:
            self.x = random.randint(0, W - 1)
            self.y = random.randint(0, H - 1)

    def draw(self):
        pygame.draw.ellipse(self.screen, (150, 150, 255), (self.x * blockW, self.y * blockH, blockW, blockH))
