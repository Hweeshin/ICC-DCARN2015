#Player
class Player:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.speed=8
        self.rect=self.surface.get_rect()
        self.pos(self.x, self.y)
    def changepos(self, changex, changey):
        self.pos(self.x+changex, self.y+changey)
    def pos(self, x,y):
        self.x=x
        self.y=y
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        screen.blit(self.surface, self.rect)
    def get_pos_x(self):
        return self.x
    def get_pos_y(self):
        return self.y
#slendy or any other enemy
class Enemy:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.speed=8
        self.rect=self.surface.get_rect()
        self.pos(self.x, self.y)
    def changepos(self, changex, changey):
        self.pos(self.x+changex, self.y+changey)
    def pos(self, x,y):
        self.x=x
        self.y=y
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        screen.blit(self.surface, self.rect)
#Solid objects
class Wall:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.rect=self.surface.get_rect()
        self.draw()
    def draw(self):
        self.rect.topleft=(self.x, self.y)
        screen.blit(self.surface, self.rect)

class Item:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.rect=self.surface.get_rect()
        self.draw()
    def draw(self):
        self.rect.topleft=(self.x, self.y)
        screen.blit(self.surface, self.rect)

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h # center player

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top

    return Rect(l, t, w, h)
# INTIALISATION
import pygame, math, sys
from pygame.locals import *
pygame.init()
screenw = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
level=[]
level = open("level.txt").read().split('\n')#Note: The width must always be equal.
size=32 #Size of one tile. It should be a square unless some idiot decides otherwise
k_up = k_down = k_left = k_right = 0
k_w = k_s = k_a = k_d = 0
BLACK = (0,0,0)
walllist=[]
listitem=[]
heighttilemax=len(level)
widthtilemax=len(level[0])
heightmax=heighttilemax*size
widthmax=widthtilemax*size
diffx=-heightmax/2
diffy=-widthmax/2
screen=pygame.Surface((widthmax, heightmax))
y=0
while(y<=heighttilemax-1):
    x=0
    while(x<=widthtilemax-1):
        if(level[y][x]=="W"):
            walllist.append(Wall(x*size, y*size, pygame.image.load('img/wall.png')))
        elif(level[y][x]=="I"):
            listitem.append(Item(x*size+8,y*size+8, pygame.image.load('img/item.png')))
        elif(level[y][x]=="P"):
            me=Player(x*size,y*size, pygame.image.load('img/player.png'))
        elif(level[y][x]=="S"):
            him=Enemy(x*size,y*size, pygame.image.load('img/enemy.png'))
        x+=1
    y+=1
    
textfont=pygame.font.SysFont("arial", 12) #test code for now, leave here for text printing
while 1:
    # USER INPUT
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN # key down or up?
        if event.key == K_RIGHT: k_right = down * me.speed
        elif event.key == K_LEFT: k_left = down * -me.speed
        elif event.key == K_UP: k_up = down * -me.speed
        elif event.key == K_DOWN: k_down = down * me.speed
        elif event.key == K_w: k_w = down * -him.speed
        elif event.key == K_s: k_s = down * him.speed
        elif event.key == K_a: k_a = down * -him.speed
        elif event.key == K_d: k_d = down * him.speed
        elif event.key == K_ESCAPE: pygame.quit()# quit the game
        #if event.type == pygame.QUIT: pygame.quit ()
    screen.fill(BLACK)
    #him.changepos(k_a+k_d, k_w+k_s)
    him.changepos(k_a+k_d, 0) #move the enemy on X axis
    x=len(walllist)-1
    if k_d+k_a<0:
        while x>=0:
            if him.rect.colliderect(walllist[x].rect)==True:
                him.pos(walllist[x].x+walllist[x].rect.width,him.y)
            x-=1
    else:
        while x>=0:
            if him.rect.colliderect(walllist[x].rect)==True:
                him.pos(walllist[x].x-him.rect.width,him.y)
            x-=1
    x=len(walllist)-1
    him.changepos(0, k_w+k_s) #move the enemy on Y axis
    if k_w+k_s<0:
          while x>=0:
            if him.rect.colliderect(walllist[x].rect)==True:
                him.pos(him.x,walllist[x].y+walllist[x].rect.height)
            x-=1
    else:
        while x>=0:
            if him.rect.colliderect(walllist[x].rect)==True:
                him.pos(him.x,walllist[x].y-him.rect.height)
            x-=1
    if(him.x<0):
        him.pos(0, me.y)
    if(him.y<0):
        him.pos(me.x, 0)

    prevx=me.x
    prevy=me.y
    me.changepos(k_left+k_right, 0) #move the player on X axis
    x=len(walllist)-1
    if k_left+k_right<0:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(walllist[x].x+walllist[x].rect.width,me.y)
            x-=1
    else:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(walllist[x].x-me.rect.width,me.y)
            x-=1
    x=len(walllist)-1
    me.changepos(0, k_down+k_up) #move the player on Y axis
    if k_up+k_down<0:
          while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(me.x,walllist[x].y+walllist[x].rect.height)
            x-=1
    else:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(me.x,walllist[x].y-me.rect.height)
            x-=1
    if(me.x<0):
        me.pos(0, me.y)
    elif(me.x+me.rect.width>widthmax):
        me.pos(widthmax-me.rect.width, me.y)
    if(me.y<0):
        me.pos(me.x, 0)
    elif(me.y+me.rect.height>heightmax):
        me.pos(me.x, heightmax-me.rect.height)
    x=len(walllist)-1
    while x>=0:
        walllist[x].draw()
        x-=1
    if me.rect.colliderect(him.rect)==True:
        print("GAME OVER")
    x=len(listitem)-1
    while x>=0:
        listitem[x].draw()
        if me.rect.colliderect(listitem[x].rect)==True:
            del listitem[x]
            print("Collected")
            if x==len(listitem)-1: x=-1
            else:
                x-=1
        else: x-=1

    newx=me.x
    newy=me.y
    diffx+=newx-prevx
    diffy+=newy-prevy
    me.draw()
    him.draw()
    screenw.blit(screen, (-diffx, -diffy))
    pygame.display.flip()
