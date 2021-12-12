import math
import random
import pygame
from PIL import Image
import tk
#from tk import messagebox

class Cube(object):
    rows = 20
    width = 500
    def __init__(self, start, dirx = 1, diry = 0, color = (255, 0, 0)):
        self.color = color
        self.pos = start
        self.dirx = 1
        self.diry = 0
        

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + diry)
        

    def draw(self, surface, eyes = False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis -2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i*dis + center - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0, 0 ,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0 ,0), circleMiddle2, radius)



class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
        

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
                elif c.diry == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
                elif c.diry == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], 0)
                else:c.move(c.dirx, c.diry)


    def reset(self, pos):
        pass

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        if dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        if dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        if dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: c.draw(surface, True)
            else: c.draw(surface)

def drawGrid(width, rows, surface):
    sizeBtwn = width // rows

    x = 0
    y = 0

    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow(surface):
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()
    
def randomSnack(rows, item):
    x = random.randrange(rows)
    y = random.randrange(rows)
    for part in item.body:
        if part.pos == (x,y): return randomSnack(rows, item)
    return (x,y)



def main():
    global width, rows, s, snack
    width = 500
    heigth = 500
    rows = 20
    s = Snake((255,0,0), (10,10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
    win = pygame.display.set_mode((width, heigth))
    clock = pygame.time.Clock()

    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
        for cube in s.body:
            if s.body[0].pos == cube.pos and cube != s.body[0]:
                flag = False
        redrawWindow(win)
    print("Votre score est de", len(s.body), "!\n")
    

main()
