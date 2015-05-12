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
        self.x+=changex
        self.y+=changey
        self.rect.move_ip(changex, changey)
    def pos(self, x,y):
        self.x=x
        self.y=y
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        screen.blit(self.surface, self.rect)
    def centrex(self):
        return self.x+(self.rect.width/2)
    def centrey(self):
        return self.y+(self.rect.height/2)
#slendy or any other enemy
class Enemy:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.dest=[]
        self.surface=surface
        self.speed=8
        self.rect=self.surface.get_rect()
        self.pos(self.x, self.y)
    def changepos(self, changex, changey):
        self.x+=changex
        self.y+=changey
        self.rect.move_ip(changex, changey)
    def pos(self, x,y):
        self.x=x
        self.y=y
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        screen.blit(self.surface, self.rect)
    def destadd(self, x, y):#Move to this COORDINATE
        self.dest.append((x,y))
    def moving(self):
        if self.dest:
            destx, desty=self.dest[0]
            if (destx, desty)==(self.x, self.y):
                self.dest.pop(0)
                self.moving()
            #distance=math.sqrt(math.pow(self.x-destx, 2) + math.pow(self.y-desty, 2))
            #unit=self.speed/distance
            #dx=(self.x-destx)*unit
            #dy=(self.y-desty)*unit
            else:
                self.pos(destx, desty)
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
windowheight=600
windowwidth=800
screenw = pygame.display.set_mode((windowwidth, windowheight))
clock = pygame.time.Clock()
level=[]
level = open("level.txt").read().split('\n')#Note: The width must always be equal.
size=32 #Size of one tile. It should be a square unless some idiot decides otherwise
k_up = k_down = k_left = k_right = 0
k_w = k_s = k_a = k_d = 0
itemcount=0
BLACK = (0,0,0)
walllist=[]
listitem=[]
heighttilemax=len(level)
widthtilemax=len(level[0])
map=[]
heightmax=heighttilemax*size
widthmax=widthtilemax*size
screen=pygame.Surface((widthmax, heightmax))
y=0
wallsurface=pygame.image.load('img/wall.png').convert()#assuming wall has no transparency
itemsurface=pygame.image.load('img/item.png').convert()#assuming item has no transparency
while(y<=heighttilemax-1):
    x=0
    while(x<=widthtilemax-1):
        if(level[y][x]=="W"):
            walllist.append(Wall(x*size, y*size, wallsurface))
        elif(level[y][x]=="I"):
            listitem.append(Item(x*size+8,y*size+8, itemsurface))
            itemcount+=1
        elif(level[y][x]=="P"):
            me=Player(x*size,y*size, pygame.image.load('img/player.png'))
        elif(level[y][x]=="S"):
            him=Enemy(x*size,y*size, pygame.image.load('img/enemy.png'))
        x+=1
    y+=1

diffx=me.centrex()-windowwidth/2
diffy=me.centrey()-windowheight/2

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
    screenw.fill(BLACK)
    screen.fill(BLACK)
    if k_a+k_d!=0 or k_w+k_s!=0:
        him.destadd(him.x+k_a+k_d, him.y+k_w+k_s)
        him.moving()

    prevx=me.x
    prevy=me.y
    me.changepos(k_left+k_right, 0) #move the player on X axis
    x=len(walllist)-1
    if k_left+k_right<0:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(walllist[x].x+walllist[x].rect.width,me.y)
                x=-1 #Skip the rest of the loop
            x-=1
    else:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(walllist[x].x-me.rect.width,me.y)
                x=-1 #Skip the rest of the loop
            x-=1
    x=len(walllist)-1
    me.changepos(0, k_down+k_up) #move the player on Y axis
    if k_up+k_down<0:
          while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(me.x,walllist[x].y+walllist[x].rect.height)
                x=-1 #Skip the rest of the loop
            x-=1
    else:
        while x>=0:
            if me.rect.colliderect(walllist[x].rect)==True:
                me.pos(me.x,walllist[x].y-me.rect.height)
                x=-1 #Skip the rest of the loop
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
            itemcount-=1
            print("Collected")
            if x==len(listitem)-1: x=-1
            else:
                x-=1
        else: x-=1
        if itemcount==0:
            print("VICTORY")

    diffx+=me.x-prevx
    diffy+=me.y-prevy
    me.draw()
    him.draw()
    screenw.blit(screen, (-diffx, -diffy))
    pygame.display.flip()
