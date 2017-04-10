import copy, pygame
from constants import *

class Snake:
    def __init__(self, x, y, screen, color):
        self.body = [[x, y]]
        self.direction = 'right'
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.tail = [x, y]
        self.screen = screen
        self.color = color

    def fixDirection(self):
        if self.dx == 1: self.direction = 'right'
        if self.dx == -1: self.direction = 'left'
        if self.dy == -1: self.direction = 'up'
        if self.dy == 1: self.direction = 'down'

    def eat(self, aim):
        return aim[0] == self.body[0][0] and aim[1] == self.body[0][1]

    def ate(self):
        self.body.append(copy.deepcopy(self.tail))
        self.score += 1
    
    def die(self, enemy):

        #coordinates of head
        x = self.body[0][0] + self.dx
        y = self.body[0][1] + self.dy
        
        #check with borders
        if x >= W or x < 0 or y >= H or y < 0:
            return 1

        #check with yourself
        for i in range(len(self.body) - 1):
            if self.body[i][0] == x and self.body[i][1] == y:
                return 1

        #check with enemy
        if [x, y] in enemy:
            return 1

        return 0


    def go(self):

        self.tail = copy.deepcopy(self.body[-1])
        i = len(self.body) - 1
        while (i > 0):
            self.body[i] = copy.deepcopy(self.body[i - 1])
            i -= 1
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        red = self.color[0]
        green = self.color[1]
        blue = self.color[2]
        k = 255 // (len(self.body) * 2)
        for b in self.body:
            pygame.draw.rect(self.screen, (red, green, blue), (b[0] * blockW, b[1] * blockH, blockW, blockH))
            if red > 100:
                red -= k
            if green > 100:
                green -= k
            if blue > 100:
                blue -= k

    def tryToDirect(self, where):
        if where == 'right' and self.direction != 'left':
            self.dx = 1
            self.dy = 0
        if where == 'left' and self.direction != 'right':
            self.dx = -1
            self.dy = 0
        if where == 'up' and self.direction != 'down':
            self.dx = 0
            self.dy = -1
        if where == 'down' and self.direction != 'up':
            self.dx = 0
            self.dy = 1
