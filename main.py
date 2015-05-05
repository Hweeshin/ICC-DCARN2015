#Player
class Player:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.speed=7
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
        self.speed=7
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
        
# INTIALISATION
import pygame, math, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
level=["W          W", "WW  I       "]#Note: The width must always be equal.
size=32 #Size of one tile. It should be a square unless some idiot decides otherwise
k_up = k_down = k_left = k_right = 0
k_w = k_s = k_a = k_d = 0
BLACK = (0,0,0)
walllist=[]
listitem=[]
heightmax=len(level)-1
widthmax=len(level[0])-1
y=0
while(y<=heightmax):
    x=0
    while(x<=widthmax):
        if(level[y][x]=="W"):
            walllist.append(Wall(x*size, y*size, pygame.image.load('img/wall.png')))
        elif(level[y][x]=="I"):
            listitem.append(Item(x*size+8,y*size+8, pygame.image.load('img/item.png')))
        x+=1
    y+=1
    
#listitem=[Item(50,100, pygame.image.load('img/item.png')), Item(200,200, pygame.image.load('img/item.png'))]
me=Player(100,100, pygame.image.load('img/player.png'))
him=Enemy(400,400, pygame.image.load('img/enemy.png'))
#walllist=[Wall(0,0, pygame.image.load('img/wall.png')), Wall(300,300, pygame.image.load('img/wall.png'))]
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
    if(me.y<0):
        me.pos(me.x, 0)
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
    me.draw()
    him.draw()
    pygame.display.flip()
