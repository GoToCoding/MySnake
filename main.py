import sys, pygame, random, copy
from snake import Snake
from food import Food
from constants import *
from ball import Ball


pygame.init()

FONT = pygame.font.SysFont("Purisa", 35)
FONT_low = pygame.font.SysFont("Purisa", 25)

icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake v1.0")
screen = pygame.display.set_mode((width, height + 40))

def faster(t):
    t -= 30
    if t < 150:
        t = 150
    return t

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
    text = FONT.render('Player1 plays with arrows', True, (150, 100, 0))
    screen.blit(text, (20, 100))

    text = FONT.render('Player2 plays with WASD keys', True, (150, 0, 100))
    screen.blit(text, (20, 250))

    text = FONT.render('Press P to start...', True, (0, 0, 100))
    screen.blit(text, (20, 400))

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

    snake1.ball = Ball(screen, snake1.color, snake2)
    snake2.ball = Ball(screen, snake2.color, snake1)

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
                if e.key == pygame.K_RCTRL:
                    snake1.ball.shot(snake1.body[0][0], snake1.body[0][1], snake1.direction)

                #second player
                if e.key == pygame.K_w:
                    snake2.tryToDirect('up')
                if e.key == pygame.K_a:
                    snake2.tryToDirect('left')
                if e.key == pygame.K_s:
                    snake2.tryToDirect('down')
                if e.key == pygame.K_d:
                    snake2.tryToDirect('right')
                if e.key == pygame.K_r:
                    snake2.ball.shot(snake2.body[0][0], snake2.body[0][1], snake2.direction)

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
        if snake1.isAlive == False:
            fl1 = False
        fl2 = snake2.die(snake1.body)
        if snake2.isAlive == False:
            fl2 = False

        if not snake1.ball.ready:
            snake1.ball.go()
        if not snake2.ball.ready:
            snake2.ball.go()

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
                stepTime = faster(stepTime)
                snake1.ate()
                yummy.removeFood(apple)
                yummy.addNew()

        #check for eating apples SECOND PLAYER
        for apple in yummy.apples:
            if snake2.eat(apple):
                stepTime = faster(stepTime)
                snake2.ate()
                yummy.removeFood(apple)
                yummy.addNew()

        screen.fill((0, 0, 0))
        # for i in range(W):
        #     for j in range(H):
        #         pygame.draw.rect(screen, (0, 0, 0), (i * blockW, j * blockH, blockW - 1, blockH - 1))

        pygame.draw.rect(screen, (30, 30, 10), (0, height, width, 40))

        snake1.draw()
        snake2.draw()
        if not snake1.ball.ready:
            snake1.ball.draw()
        if not snake2.ball.ready:
            snake2.ball.draw()
        yummy.draw()

        text = FONT_low.render('Player1 score: ' + str(snake1.score), True, (255, 255, 0))
        screen.blit(text, (20, height))

        text = FONT_low.render('Player2 score: ' + str(snake2.score), True, (255, 0, 255))
        screen.blit(text, (340, height))

        pygame.display.update()


if __name__ == '__main__':
    game()
    