class Player:
    def __init__(self,x1,y1):
        self.x=x1
        self.y=y1
        self.speed=5
    def pos(self, x1,y1):
        self.x=x1
        self.y=y1
        self.draw()
    def draw(self):
        rect = guyimg.get_rect()
        rect.topleft = (self.x, self.y)
        screen.blit(guyimg, rect)

class Wall:
    def __init__(self,x1,y1):
        self.x=x1
        self.y=y1
        self.draw()
    def draw(self):
        wall1=wallimg.get_rect()
        wall1.topleft=(self.x, self.y)
        screen.blit(wallimg, wall1)
        
# INTIALISATION
import pygame, math, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
guyimg = pygame.image.load('img/player.png')
wallimg = pygame.image.load('img/wall.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
x=y=100 #spawn location
BLACK = (0,0,0)
me=Player(x,y)
newwall=Wall(0,0)
textfont=pygame.font.SysFont("arial", 12)
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
        elif event.key == K_ESCAPE: pygame.quit ()# quit the game
        #if event.type == pygame.QUIT: pygame.quit ()
    screen.fill(BLACK)
    
    # SIMULATION
    x += k_left+k_right
    y += k_down+k_up
    # RENDERING
    me.pos(x, y)
    #if((guyimg.get_rect()).colliderect(wallimg.get_rect())):
    #    print("Collided")
    newwall.draw()
    
    pygame.display.flip()
