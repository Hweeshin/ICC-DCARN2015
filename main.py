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
        self.draw()
    def draw(self):
        self.rect.topleft = (self.x, self.y)
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
newwall=Wall(0,0, pygame.image.load('img/wall.png'))
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
    currentx=me.x
    currenty=me.y
    me.changepos(k_left+k_right, k_down+k_up) #move the player to the new location
    if me.rect.colliderect(newwall.rect)==True:
        print("Collided")
    newwall.draw()
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
    
    pygame.display.flip()
