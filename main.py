#Player
class Player:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.speed=5
    def changepos(self, changex, changey):
        self.pos(self.x+changex, self.y+changey)
    def pos(self, x,y):
        self.x=x
        self.y=y
        self.draw()
    def draw(self):
        rect = self.surface.get_rect()
        rect.topleft = (self.x, self.y)
        screen.blit(self.surface, rect)
#Solid objects
class Wall:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.surface=surface
        self.draw()
    def draw(self):
        wall1=self.surface.get_rect()
        wall1.topleft=(self.x, self.y)
        screen.blit(self.surface, wall1)
        
# INTIALISATION
import pygame, math, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
BLACK = (0,0,0)
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
    
    me.changepos(k_left+k_right, k_down+k_up) #move the player to the new location
    #if((me.surface.get_rect()).colliderect(newwall.surface.get_rect())==True):
    #    print("Collided")
    newwall.draw()
    
    pygame.display.flip()
