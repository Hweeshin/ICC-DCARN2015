class player:
    def __init__(self,x1,y1):
        self.x=x1
        self.y=y1
        self.speed=5
    def pos(self, x1,y1):
        self.x=x1
        self.y=y1
        self.draw()
    def draw(self):
        rect = guy.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(guy, rect)


# INTIALISATION
import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768))
guy = pygame.image.load('car.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
x=y=100 #spawn location
BLACK = (0,0,0)
me=player(x,y)

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
    # .. new position based on current position, speed and direction
    x += k_left+k_right
    y += k_down+k_up
    
    # RENDERING
    # .. position the car on screen
    me.pos(x, y)
    # .. render the car to screen
    pygame.display.flip()
