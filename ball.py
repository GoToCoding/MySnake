import copy, pygame
from constants import *

class Ball:
	def __init__(self, screen, color, enemy):
		self.ready = True
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.screen = screen
		r = color[0] - 100
		if r < 0:
			r = 0
		g = color[1] - 100
		if g < 0:
			g = 0
		b = color[2] - 100
		if b < 0:
			b = 0		
		self.color = (r, g, b)
		self.enemy = enemy
	
	def shot(self, x, y, direction):
		if self.ready != False:
			self.x = x
			self.y = y
			self.ready = False
			if direction == 'right':
				self.dx = 1
				self.dy = 0
			if direction == 'left':
				self.dx = -1
				self.dy = 0
			if direction == 'up':
				self.dx = 0
				self.dy = -1
			if direction == 'down':
				self.dx = 0
				self.dy = 1

			self.go()

	def go(self):
		self.x += self.dx
		self.y += self.dy
		if self.x < 0 or self.x >= W or self.y < 0 or self.y >= H:
			self.ready = True

		if [self.x, self.y] in self.enemy.body:
			self.ready = False
			if self.enemy.body[0][0] == self.x and self.enemy.body[0][1] == self.y:
				self.enemy.isAlive = False
			else:
				newBody = []
				for b in self.enemy.body:
					if b[0] == self.x and b[1] == self.y:
						break
					newBody.append(b)
				self.enemy.body = newBody

	def draw(self):
		pygame.draw.ellipse(self.screen, self.color, (self.x * blockW, self.y * blockH, blockW, blockH))