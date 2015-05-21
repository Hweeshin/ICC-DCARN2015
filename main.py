import math, random
def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
#Player
class Player:
    def __init__(self,x,y, surface):
        self.x=x
        self.y=y
        self.originalx=x
        self.originaly=y
        self.surface=surface
        self.speed=8
        self.vision=6#change this if vision changes
        self.itemcollected=0
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
    def tilex(self, tilesize):
        return math.ceil(self.x/tilesize)
    def tiley(self, tilesize):
        return math.ceil(self.y/tilesize)
    def respawn(self):
        self.pos(self.originalx, self.originaly)
#slendy or any other enemy
class Enemy:
    def __init__(self,x,y, surfaces):
        self.x=x
        self.y=y
        self.dest=[]
        self.index=0
        self.surfaces=surfaces
        self.speed=8
        self.chasing=False #Not chasing the player
        self.level=0#0 is lowest, 2 is highest
        self.rect=self.surfaces[self.index].get_rect()
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
        screen.blit(self.surfaces[self.index], self.rect)
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
    def levelset(self, newlevel):
        self.level=newlevel
    def wheretogo(self, playerx, playery, tilex, tiley, playervision):
        if self.level==0:
            self.pos(playerx+size*playervision, playery+size*playervision)
        elif self.level==1:
            random.seed()
            random.randint(-playervision, playervision)
    def gettiley(self, tilexdiff, distance):
        random.seed()
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

class texture:
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

def reset(playerobj):
    playerobj.respawn()

# INTIALISATION
import pygame, sys
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
tilemap={}#yes guys I am using a dictionary, shit is going down
heightmax=heighttilemax*size
widthmax=widthtilemax*size
screen=pygame.Surface((widthmax, heightmax))
vision=pygame.image.load('img/vision6.png')
visionrect=vision.get_rect()
play_normal=pygame.image.load('img/Play_normal.png').convert()
playrect=play_normal.get_rect()
play_highlighted=pygame.image.load('img/Play_highlighted.png').convert()
playrect.topleft=(330, 350)
slendyman=pygame.image.load('img/slendyman.png').convert()
slendymanrect=slendyman.get_rect()
slendymanrect.topleft=(100,130)
victory=pygame.image.load('img/victory.png').convert()
victoryrect=victory.get_rect()
victoryrect.topleft=(50,190)
mainmenu_normal=pygame.image.load('img/mainmenu_normal.png').convert()
mainmenurect=mainmenu_normal.get_rect()
mainmenu_highlighted=pygame.image.load('img/mainmenu_highlighted.png').convert()
mainmenurect.topleft=(470, 425)
gameover=pygame.image.load('img/gameover.png').convert()
gameoverrect=gameover.get_rect()
gameoverrect.topleft=(80,200)
y=0
wallsurface=pygame.image.load('img/wall.png').convert()#assuming wall has no transparency
itemsurface=pygame.image.load('img/pages.png')
while(y<=heighttilemax-1):
    x=0
    while(x<=widthtilemax-1):
        if(level[y][x]=="W"):
            walllist.append(Wall(x*size, y*size, wallsurface))
        elif(level[y][x]=="I"):
            listitem.append(Item(x*size+8,y*size+8, itemsurface))
        elif(level[y][x]=="P"):
            me=Player(x*size,y*size, pygame.image.load('img/player.png'))
        elif(level[y][x]=="S"):
            him=Enemy(x*size,y*size, [pygame.image.load('img/slender1.png'), pygame.image.load('img/slender2.png'), pygame.image.load('img/slender3.png'), pygame.image.load('img/slender4.png'), pygame.image.load('img/slender5.png')])
        x+=1
    y+=1
itemcount=len(listitem)
totalitem=itemcount
diffx=me.centrex()-windowwidth/2
diffy=me.centrey()-windowheight/2
gamestate=0#0 is main menu, 1 is death screen, 2 is victory screen, 3 is playing
animtick=0
listitembackup=list(listitem)

while 1:
    # USER INPUT
    clock.tick(30)
    button1=button2=button3=False
    if gamestate==0:
        for event in pygame.event.get():
            if hasattr(event, 'key'):
                if event.key == K_ESCAPE: pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (button1, button2, button3)=pygame.mouse.get_pressed()
        screenw.fill(BLACK)
        screenw.blit(slendyman, slendymanrect)
        (mousex, mousey)=pygame.mouse.get_pos()
        if playrect.collidepoint(mousex, mousey):
            screenw.blit(play_highlighted, playrect)
            if button1==True:
                reset(me)
                diffx=me.centrex()-windowwidth/2
                diffy=me.centrey()-windowheight/2
                k_up = k_down = k_left = k_right = 0
                listitem=list(listitembackup)
                itemcount=len(listitem)
                gamestate=3
        else:
            screenw.blit(play_normal, playrect)
        pygame.display.flip()
    if gamestate==1:
        for event in pygame.event.get():
            if hasattr(event, 'key'):
                if event.key == K_ESCAPE: pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (button1, button2, button3)=pygame.mouse.get_pressed()
        screenw.fill(BLACK)
        screenw.blit(gameover, gameoverrect)
        (mousex, mousey)=pygame.mouse.get_pos()
        if mainmenurect.collidepoint(mousex, mousey):
            screenw.blit(mainmenu_highlighted, mainmenurect)
            if button1==True:
                gamestate=0
        else:
            screenw.blit(mainmenu_normal, mainmenurect)
        pygame.display.flip()
    if gamestate==2:
        for event in pygame.event.get():
            if hasattr(event, 'key'):
                if event.key == K_ESCAPE: pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (button1, button2, button3)=pygame.mouse.get_pressed()
        screenw.fill(BLACK)
        screenw.blit(victory, victoryrect)
        (mousex, mousey)=pygame.mouse.get_pos()
        if mainmenurect.collidepoint(mousex, mousey):
            screenw.blit(mainmenu_highlighted, mainmenurect)
            if button1==True:
                gamestate=0
        else:
            screenw.blit(mainmenu_normal, mainmenurect)
        pygame.display.flip()
    if gamestate==3:
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN # key down or up?
            if event.key == K_RIGHT: k_right = down * me.speed
            elif event.key == K_LEFT: k_left = down * -me.speed
            elif event.key == K_UP: k_up = down * -me.speed
            elif event.key == K_DOWN: k_down = down * me.speed
            elif event.key == K_ESCAPE: pygame.quit()# quit the game
        screen.fill(BLACK)
        #if k_a+k_d!=0 or k_w+k_s!=0:
        #    him.destadd(him.x+k_a+k_d, him.y+k_w+k_s)
        #    him.moving()
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
            gamestate=1
        x=len(listitem)-1
        while x>=0:
            listitem[x].draw()
            if me.rect.colliderect(listitem[x].rect)==True:
                del listitem[x]
                itemcount-=1
                print("Collected")#TODO: IMPLEMENT AN ACTUAL PAGE TO READ
                if x==len(listitem)-1: x=-1
                else:
                    x-=1
            else: x-=1
            if itemcount==0:
                gamestate=2
        diffx+=me.x-prevx
        diffy+=me.y-prevy
        him.levelset(totalitem-itemcount)
        him.wheretogo(me.x, me.y, me.tilex(size), me.tiley(size), me.vision)
        me.draw()
        him.draw()
        if animtick<2:
            animtick+=1
        else:
            animtick=0
            if him.index<4:
                him.index+=1
            else:
                him.index=0
        visionrect.center=me.rect.center
        screen.blit(vision, visionrect)
        screenw.blit(screen, (-diffx, -diffy))
        pygame.display.flip()
