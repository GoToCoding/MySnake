import copy, pygame, random
from constants import *

#	TODO:
# - need unique apples

class Food:

    def __init__(self, cnt, SCREEN):
        self.apples = []
        for i in range(cnt):
        	self.apples.append([random.randint(0, W - 1), random.randint(0, H - 1)])
        self.screen = SCREEN

    def addNew(self):
        self.apples.append([random.randint(0, W - 1), random.randint(0, H - 1)])
    
    def removeFood(self, food):
    	self.apples.remove(food)

    def draw(self):
    	for apple in self.apples:
        	pygame.draw.ellipse(self.screen, (150, 150, 255), (apple[0] * blockW, apple[1] * blockH, blockW, blockH))
