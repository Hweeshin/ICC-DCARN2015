#Player
class Player:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.speed=5
        self.rect=self.surface.get_rect()
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
k_up = k_down = k_left = k_right = 0
BLACK = (0,0,0)
listitem=[Item(50,100, pygame.image.load('img/item.png')), Item(200,200, pygame.image.load('img/item.png'))]
me=Player(100,100, pygame.image.load('img/player.png'))
walllist=[Wall(0,0, pygame.image.load('img/wall.png')), Wall(300,300, pygame.image.load('img/wall.png'))]
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
        elif event.key == K_ESCAPE: pygame.quit()# quit the game
        #if event.type == pygame.QUIT: pygame.quit ()
    screen.fill(BLACK)
    me.changepos(k_left+k_right, 0) #move the player to the new location
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
    me.changepos(0, k_down+k_up) #move the player to the new location
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
    x=len(walllist)-1
    while x>=0:
        walllist[x].draw()
        x-=1
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
    pygame.display.flip()
