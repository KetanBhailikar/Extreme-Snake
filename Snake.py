import pygame
import time
import random

#global variables
keypress = []
sizw = 400
done = True
pygame.init()
pygame.display.set_caption('Snake')
win = pygame.display.set_mode((sizw+2, sizw + 22))
dirx = 1
diry = 0
x = 2
y = 22
fx = -20
fy = -20
end = 0
tk = time.time()
ad = 0
food = True
siz = 20
dificulty = 2
tail = [[2, 22], [2, 22], [2, 22], [2, 22]]
t0 = time.time()


def giveFood():  # randomly produce food
    global food, fx, fy, sizw
    if food:
        fx = random.randint(0, (sizw//20)-1) * 20 + 2
        fy = random.randint(0, (sizw//20)-1) * 20 + 22
        food = False


def checkEndOfGame():  # check if the player died
    global done, sizw
    if x <= 0 or y <= 20 or x >= sizw or y >= (sizw+20) or ((tail[0] in tail[2:]) and len(tail) != 1):
        done = False


def draw():  # draw the boxes,snake and its food
    global t0, siz, tail, food, x, y, dificulty, tk, done, dirx, diry, end, sizw

    # draw the background
    pygame.draw.rect(win, (173, 184, 141), pygame.Rect(0, 0, sizw+2, sizw+42))
    t0 = time.time()

    # keypresses are queued
    if len(keypress) != 0:
        if keypress[-1] == "u":
            if diry != 1:
                diry = -1
                dirx = 0
                keypress.remove(keypress[0])
        elif keypress[-1] == "d":
            if diry != -1:
                diry = 1
                dirx = 0
                keypress.remove(keypress[0])
        elif keypress[-1] == "r":
            if dirx != -1:
                dirx = 1
                diry = 0
                keypress.remove(keypress[0])
        elif keypress[-1] == "l":
            if dirx != 1:
                dirx = -1
                diry = 0
                keypress.remove(keypress[0])

    # update the position of the snake
    x += dirx*siz
    y += diry*siz

    # check if the snake gets the food
    if x == fx and y == fy:
        tail.append([400, 400])
        tk = time.time()
        dificulty += 1
        food = True

    # Start the timer to make the game more difficult
    if len(tail) >= 6:
        ts = str(7-int(time.time() - tk))
    else:
        ts = " - "
    if ts != " - ":
        if int(ts) < 0:
            done = False

    # assign a random position to the food
    giveFood()

    # print the score, "Snake", and time left
    font1 = pygame.font.Font('freesansbold.ttf', 18)
    font2 = pygame.font.Font('freesansbold.ttf', 16)
    score1 = font1.render('Score : '+str(len(tail)-4),
                          True, (60, 65, 49), (173, 184, 141))
    nam = font1.render('Snake', True,  (60, 65, 49), (173, 184, 141))
    tl = font2.render('Time Left : '+ts, True,  (60, 65, 49), (173, 184, 141))
    s3rect = tl.get_rect()
    s2rect = nam.get_rect()
    s1rect = score1.get_rect()
    s1rect.center = (45, 11)
    s2rect.center = ((sizw+2)/2, 11)
    s3rect.center = (sizw-58, 11)
    win.blit(score1, s1rect)
    win.blit(nam, s2rect)
    win.blit(tl, s3rect)

    # draw the boxes
    for i in range(22, sizw+20, siz):
        for j in range(2, sizw, siz):
            pygame.draw.rect(win, (197, 209, 164),
                             pygame.Rect(j, i, siz-2, siz-2))

    # draw the head of the snake
    pygame.draw.rect(win, (60, 65, 49), pygame.Rect(x, y, siz-2, siz-2))
    pygame.draw.rect(win, (173, 184, 141),
                     pygame.Rect(x+3, y+3, siz-8, siz-8))
    pygame.draw.rect(win, (60, 65, 49), pygame.Rect(x+5, y+5, siz-12, siz-12))

    # draw the food
    pygame.draw.rect(win, (60, 65, 49), pygame.Rect(
        fx+4, fy+4, siz-10, siz-10))

    # draw the entire tail
    for k in tail[:-1]:
        pygame.draw.rect(win, (60, 65, 49),
                         pygame.Rect(k[0], k[1], siz-2, siz-2))
        pygame.draw.rect(win, (173, 184, 141),
                         pygame.Rect(k[0]+3, k[1]+3, siz-8, siz-8))
        pygame.draw.rect(win, (60, 65, 49), pygame.Rect(
            k[0]+5, k[1]+5, siz-12, siz-12))

    # update the positions of each part of the tail
    for k in range(len(tail)):
        if k == 0:
            tail[k][0] = x
            tail[k][1] = y
        else:
            tail[-k][0] = tail[-k-1][0]
            tail[-k][1] = tail[-k-1][1]


def main():  # driver code
    global t1, t0, dirx, diry, done, end

    # game loop
    while done:

        # incrementing the snake after only a fixed amount of time
        t1 = time.time()
        if t1 - t0 >= (1/dificulty):
            draw()
            checkEndOfGame()

        # loop through game events and check for keypresses
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = False
                end = 1
            if e.type == pygame.KEYDOWN:
                k = pygame.key.get_pressed()
                if k[pygame.K_UP]:
                    keypress.append("u")
                k = pygame.key.get_pressed()
                if k[pygame.K_DOWN]:
                    keypress.append("d")
                k = pygame.key.get_pressed()
                if k[pygame.K_RIGHT]:
                    keypress.append("r")
                k = pygame.key.get_pressed()
                if k[pygame.K_LEFT]:
                    keypress.append("l")
        pygame.display.flip()

    # show the game over screen only if the player loses and not if he wants to quit
    if end == 0:
        again()


def again():  # game over screen
    global t0, done, tail, dirx, diry, fx, fy, food, x, y, ad, dificulty, sizw
    sl = 0
    doe = True

    # Set the text that is to be shown on the screen
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Game Over', True, (255, 255, 255), (0, 0, 0))
    score = font.render('Score : '+str(len(tail)-4),
                        True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    srect = score.get_rect()
    srect.center = ((sizw+2) // 2, (sizw+42-80) // 2)
    textRect.center = ((sizw+2) // 2, (sizw+42) // 2)

    # screen loop
    while doe:

        # show the score and "Game Over" on the screen
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, sizw+2, sizw+42))
        win.blit(text, textRect)
        win.blit(score, srect)

        # end this loop if player presses space
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            doe = False
            sl = 1

        # exit if the Close Button is Pressed
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                doe = False

        pygame.display.flip()

    # reset all the variables and restart if the player presses Space Bar
    if sl == 1:
        dirx = 1
        diry = 0
        x = 2
        y = 22
        fx = -20
        end = 0
        fy = -20
        ad = 0
        food = True
        siz = 20
        dificulty = 2
        tail = [[2, 22], [2, 22], [2, 22], [2, 22]]
        t0 = time.time()
        done = True
        main()


main()
