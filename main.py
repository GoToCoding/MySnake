import sys, pygame, random, copy
from snake import Snake
from food import Food
from constants import *


pygame.init()

FONT = pygame.font.SysFont("Purisa", 40)
FONT_low = pygame.font.SysFont("Purisa", 25)

icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake v1.0")
screen = pygame.display.set_mode((width, height + 40))

def TheEnd(name, score):

    screen.fill((40, 255, 50))       

    text = FONT.render('The end!', True, (100, 100, 100))
    screen.blit(text, (50, 50))

    if name == 'Draw':
        text = FONT.render('Draw!', True, (100, 100, 100))
        screen.blit(text, (50, 120))
    else:
        text = FONT.render(name + ' win!', True, (100, 100, 100))
        screen.blit(text, (50, 120))

        text = FONT.render('Score: ' + str(score), True, (100, 100, 100))
        screen.blit(text, (50, 190))

    text = FONT.render('Press ECS to exit...', True, (100, 100, 100))
    screen.blit(text, (50, 260))

    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()

def menu():
    screen.fill((40, 255, 50))
    text = FONT.render('Player1 plays with arrows', True, (100, 100, 100))
    screen.blit(text, (40, 100))

    text = FONT.render('Player2 plays with WASD keys', True, (100, 100, 100))
    screen.blit(text, (40, 350))
    pygame.display.update()
    inMenu = True
    while inMenu:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    inMenu = False

def game():

    menu()
    for i in range(W):
        for j in range(H):
            pygame.draw.rect(screen, (0, 0, 0), (i * blockW, j * blockH, blockW - 1, blockH - 1), 2)
    
    pygame.display.update()

    lastStep = 0
    stepTime = 300

    snake1 = Snake(2, 2, screen, (255, 255, 0))
    snake2 = Snake(20, 20, screen, (255, 0, 255))
    yummy = Food(25, screen)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                sys.exit()
            if e.type == pygame.KEYDOWN:
                
                #first player
                if e.key == pygame.K_UP:
                    snake1.tryToDirect('up')
                if e.key == pygame.K_DOWN:
                    snake1.tryToDirect('down')
                if e.key == pygame.K_LEFT:
                    snake1.tryToDirect('left')
                if e.key == pygame.K_RIGHT:
                    snake1.tryToDirect('right')

                #second player
                if e.key == pygame.K_w:
                    snake2.tryToDirect('up')
                if e.key == pygame.K_a:
                    snake2.tryToDirect('left')
                if e.key == pygame.K_s:
                    snake2.tryToDirect('down')
                if e.key == pygame.K_d:
                    snake2.tryToDirect('right')

                #pause
                if e.key == pygame.K_p:
                    pause = True
                    while pause:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                sys.exit()
                            if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_p:
                                    pause = False

        if lastStep + stepTime > pygame.time.get_ticks():
            continue
        lastStep = pygame.time.get_ticks()

        snake1.fixDirection()
        snake2.fixDirection()

        fl1 = snake1.die(snake2.body)
        fl2 = snake2.die(snake1.body)

        snake1.go()
        snake2.go()

        #FIXME (Spike: If heads are equal I check it like this)
        if (fl1 and fl2) or (snake1.body[0][0] == snake2.body[0][0] and snake1.body[0][1] == snake2.body[0][1]):
            if snake1.score > snake2.score:
                TheEnd('Player 1', snake1.score)
            elif snake1.score < snake2.score:
                TheEnd('Player 2', snake2.score)
            else:
                TheEnd('Draw', snake1.score)
        if fl1:
            TheEnd('Player 2', snake2.score)
        if fl2:
            TheEnd('Player 1', snake1.score)

        #check for eating apples FIRST  PLAYER
        for apple in yummy.apples:
            if snake1.eat(apple):
                snake1.ate()
                yummy.removeFood(apple)
                yummy.addNew()

        #check for eating apples SECOND PLAYER
        for apple in yummy.apples:
            if snake2.eat(apple):
                snake2.ate()
                yummy.removeFood(apple)
                yummy.addNew()

        screen.fill(GREEN)
        for i in range(W):
            for j in range(H):
                pygame.draw.rect(screen, (0, 0, 0), (i * blockW, j * blockH, blockW - 1, blockH - 1))

        snake1.draw()
        snake2.draw()
        yummy.draw()

        text = FONT_low.render('Player1 score: ' + str(snake1.score), True, (100, 100, 100))
        screen.blit(text, (20, 600))

        text = FONT_low.render('Player2 score: ' + str(snake2.score), True, (100, 100, 100))
        screen.blit(text, (400, 600))

        pygame.display.update()


if __name__ == '__main__':
    game()
    