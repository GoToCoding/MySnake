import sys, pygame, random, copy
from snake import Snake
from food import Food
from constants import *


pygame.init()

FONT = pygame.font.SysFont("Purisa", 40)
FONT_low = pygame.font.SysFont("Purisa", 25)

screen = pygame.display.set_mode((width, height + 40))
pygame.display.set_caption("Snake v0.1")

def TheEnd(score):
    screen.fill((40, 255, 50))
    text = FONT.render('The end!', True, (100, 100, 100))
    screen.blit(text, (50, 50))

    text = FONT.render('Your score: ' + str(score), True, (100, 100, 100))
    screen.blit(text, (50, 100))

    text = FONT.render('Press ECS to exit...', True, (100, 100, 100))
    screen.blit(text, (50, 200))

    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()

def game():

    for i in range(W):
        for j in range(H):
            pygame.draw.rect(screen, (0, 0, 0), (i * blockW, j * blockH, blockW - 1, blockH - 1), 2)


    pygame.display.update()

    lastStep = 0
    stepTime = 400

    snake = Snake(2, 2, screen)
    apple = Food(4, 2, screen)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and snake.direction != 'down': 
                    snake.dx = 0
                    snake.dy = -1
                if e.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.dx = 0
                    snake.dy = 1
                if e.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.dx = 1
                    snake.dy = 0
                if e.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.dx = -1
                    snake.dy = 0

        if lastStep + stepTime > pygame.time.get_ticks():
            continue
        lastStep = pygame.time.get_ticks()

        snake.fixDirection()

        if snake.die():
            TheEnd(snake.score)
            sys.exit()

        snake.go()
        if snake.eat(apple):
            stepTime -= 25
            if stepTime < 120: stepTime = 120
            snake.ate(apple)
            apple.getNew(snake.body)

        screen.fill(GREEN)
        for i in range(W):
            for j in range(H):
                pygame.draw.rect(screen, (0, 0, 0), (i * blockW, j * blockH, blockW - 1, blockH - 1))

        snake.draw()
        apple.draw()

        text = FONT_low.render('Score: ' + str(snake.score), True, (100, 100, 100))
        screen.blit(text, (30, 600))

        pygame.display.update()


if __name__ == '__main__':
    game()
    