import pygame
import random
import time
pygame.init()


keyQ = []                   # key presses are queued
screenSize = 400            # screen Size
boxSize = 20                # size of grid boxes
difficulty = 2              # difficulty of the game
foodPos = (-1,-1)           # position of the food
isFoodPresent = False       # is food on the board
lastTimeEaten = time.time() # track the time left to eat
lost = False                # did the player lose



class Snake:
    def __init__(self):     # snake's attributes 
        self.head = (62,22)
        self.tail = [[42,22],[22,22],[2,22]]
        self.dirx = 1
        self.diry = 0
    
    def drawSnake(self,screen):     # draw the snake on the board
        pygame.draw.rect(screen, (60, 65, 49), pygame.Rect(self.head[0], self.head[1],boxSize-2,boxSize-2))
        pygame.draw.rect(screen, (173, 184, 141),pygame.Rect(self.head[0]+3, self.head[1]+3, boxSize-8, boxSize-8))
        pygame.draw.rect(screen, (60, 65, 49), pygame.Rect(self.head[0]+5, self.head[1]+5, boxSize-12, boxSize-12))
        for k in self.tail:
            pygame.draw.rect(screen, (60, 65, 49),pygame.Rect(k[0], k[1], boxSize-2, boxSize-2))
            pygame.draw.rect(screen, (173, 184, 141),pygame.Rect(k[0]+3, k[1]+3, boxSize-8, boxSize-8))
            pygame.draw.rect(screen, (60, 65, 49), pygame.Rect(k[0]+5, k[1]+5, boxSize-12, boxSize-12))
    
    def updateSnake(self):          # update snake's position
        global keyQ
        if len(keyQ) != 0:
            if keyQ[0] == "u":
                if self.diry != 1:
                    self.diry = -1
                    self.dirx = 0
                    keyQ.remove(keyQ[0])
            elif keyQ[0] == "d":
                if self.diry != -1:
                    self.diry = 1
                    self.dirx = 0
                    keyQ.remove(keyQ[0])
            elif keyQ[0] == "r":
                if self.dirx != -1:
                    self.dirx = 1
                    self.diry = 0
                    keyQ.remove(keyQ[0])
            elif keyQ[0] == "l":
                if self.dirx != 1:
                    self.dirx = -1
                    self.diry = 0
                    keyQ.remove(keyQ[0])
        for k in range(len(self.tail)-1):
            self.tail[-(k+1)][0] = self.tail[-(k+1)-1][0]
            self.tail[-(k+1)][1] = self.tail[-(k+1)-1][1]
        self.tail[0][0] = self.head[0]
        self.tail[0][1] = self.head[1]
        self.head = (self.head[0] + (self.dirx * boxSize) , self.head[1] + (self.diry * boxSize))

    def putFood(self,screen):       # put food on the screen randomly
        global foodPos, isFoodPresent
        if isFoodPresent == False:
            fx = random.randint(0, (screenSize/20)-1) * 20 + 2
            fy = random.randint(0, (screenSize/20)-1) * 20 + 22
            foodPos = (fx,fy)
            isFoodPresent = True
        pygame.draw.rect(screen, (60, 65, 49), pygame.Rect(foodPos[0]+4, foodPos[1]+4, boxSize-10, boxSize-10))
    
    def eatFood(self):              # check if the food is eaten
        global difficulty, isFoodPresent,lastTimeEaten
        if self.head == foodPos:
            self.tail.append([400, 400])
            difficulty += 1
            lastTimeEaten = time.time()
            isFoodPresent = False

    def checkDeath(self):           # check if the snake died
        global lost
        if self.head[0] < -20 or self.head[1] < 20 or self.head[0] >= screenSize or self.head[1] >= screenSize+20 or (([self.head[0],self.head[1]] in self.tail)):
            lost = True
            return True
        return False


def drawGrid(screen, screenSize):   # draw the grid on the screen
    # draw the background
    pygame.draw.rect(screen, (173, 184, 141), pygame.Rect(0, 0, screenSize+2, screenSize+22))

    # draw the grid
    for i in range(22, screenSize+20, 20):
        for j in range(2, screenSize, 20):
            pygame.draw.rect(screen, (197, 209, 164),pygame.Rect(j, i, boxSize-2, boxSize-2))

def showText(screen,tim,s):         # show the text on the screen
    font1 = pygame.font.Font('freesansbold.ttf', 18)
    font2 = pygame.font.Font('freesansbold.ttf', 16)
    score1 = font1.render('Score : '+str(len(s.tail)-3),True, (60, 65, 49), (173, 184, 141))
    nam = font1.render('Snake', True,  (60, 65, 49), (173, 184, 141))
    if len(s.tail) >= 5:
        t = tim
    else:
        t = " - "
    tl = font2.render('Time Left : '+str(t), True,  (60, 65, 49), (173, 184, 141))
    s3rect = tl.get_rect()
    s2rect = nam.get_rect()
    s1rect = score1.get_rect()
    s1rect.center = (45, 11)
    s2rect.center = ((screenSize+2)/2, 11)
    s3rect.center = ((screenSize+2)-60, 11)
    screen.blit(score1, s1rect)
    screen.blit(nam, s2rect)
    screen.blit(tl, s3rect)

def gameOverScreen(screen,score):   # show the game over screen and restart if space is pressed
    global difficulty,foodPos,isFoodPresent,lastTimeEaten,lost
    loop = True
    restart = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Game Over', True, (255, 255, 255), (0, 0, 0))
    score = font.render('Score : '+str(score),True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    srect = score.get_rect()
    srect.center = ((screenSize+2) // 2, (screenSize+42-80) // 2)
    textRect.center = ((screenSize+2) // 2, (screenSize+42) // 2)
    while loop:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenSize+2, screenSize+42))
        screen.blit(text, textRect)
        screen.blit(score, srect)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            loop = False
            restart = 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                loop = False
        pygame.display.flip()
    if restart == 1:
        difficulty = 3
        foodPos = (-1,-1)
        isFoodPresent = False
        lastTimeEaten = time.time()
        lost = False
        main()

def main():             # main code
    global lost,keyQ
    s = Snake()
    pygame.display.set_caption('Snake')
    win = pygame.display.set_mode((screenSize+2, screenSize+22))
    loop = True
    t0 = 0
    while loop:         # game loop
        if time.time() - t0 >= 1/difficulty:
            drawGrid(win,screenSize)
            s.updateSnake()
            s.drawSnake(win)
            s.eatFood()
            s.putFood(win)
            showText(win,7-int(time.time()-lastTimeEaten),s)
            if 7-int(time.time()-lastTimeEaten) <= 0 and len(s.tail) >= 5:
                loop = False
                lost = True
            if s.checkDeath():
                loop = False
                lost = True
            t0 = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                loop = False
            k = pygame.key.get_pressed()
            if k[pygame.K_UP] and len(keyQ) <=1:
                keyQ.append("u")
            if k[pygame.K_DOWN] and len(keyQ) <=1:
                keyQ.append("d")
            if k[pygame.K_RIGHT] and len(keyQ) <=1:
                keyQ.append("r")
            if k[pygame.K_LEFT] and len(keyQ) <=1:
                keyQ.append("l")
        pygame.display.flip()
    
    if lost:    
        gameOverScreen(win,len(s.tail)-3)
main()
