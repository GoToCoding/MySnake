import copy, pygame
from constants import *

class Snake:
    def __init__(self, x, y, SCREEN):
        self.body = [[x, y]]
        self.direction = 'right'
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.tail = [x, y]
        self.screen = SCREEN

    def fixDirection(self):
        if self.dx == 1: self.direction = 'right'
        if self.dx == -1: self.direction = 'left'
        if self.dy == -1: self.direction = 'up'
        if self.dy == 1: self.direction = 'down'

    def eat(self, aim):
        return ([aim.x, aim.y] in self.body)

    def ate(self, aim):
        self.body.append(copy.deepcopy(self.tail))
        self.score += 1
    
    def die(self):
        x = self.body[0][0] + self.dx
        y = self.body[0][1] + self.dy
        if x >= W or x < 0 or y >= H or y < 0:
            return 1
        for i in range(len(self.body)):
            j = i + 1
            while j < len(self.body):
                if self.body[i][0] == self.body[j][0] and self.body[i][1] == self.body[j][1]:
                    return 1
                j += 1
        return 0

    def go(self):
        self.tail = copy.deepcopy(self.body[-1])
        i = len(self.body) - 1
        while (i > 0):
            self.body[i] = copy.copy(self.body[i - 1])
            i -= 1
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        red = 155
        blue = 100
        k = red / (len(self.body))
        for b in self.body:
            pygame.draw.rect(self.screen, (red, 50, blue), (b[0] * blockW, b[1] * blockH, blockW, blockH))
            red -= k
            blue += k
