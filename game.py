import sys
import os
import pygame
import math
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, gs=None):
                pygame.sprite.Sprite.__init__(self)
                pygame.key.set_repeat(1,50)
                self.gs = gs
                self.image = pygame.image.load("deathstar.png")
                self.rect = self.image.get_rect()
                self.rect.center = (300,300)
                self.orig_image = self.image
                self.tofire = False
        
    def tick(self):
        if self.tofire == True:
            return 0

        else:
            mx, my = pygame.mouse.get_pos()
            rx, ry = self.rect.center
            opp = mx - rx
            adj = my - ry
            angle = math.atan2(opp,adj) 
            angle *=(180/math.pi)
            #print(angle)
            self.image = pygame.transform.rotate(self.image,angle/60)
            self.rect = self.image.get_rect(center=self.rect.center)

    def move(self,x,y):
        self.rect = self.rect.move(x,y)
        

class Laser(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.sprites = []
        self.images = []
        self.firing = False

    def tick(self):
        for i in range(len(self.sprites)):
            self.sprites[i] = self.sprites[i].move(3,3)
        if self.firing == False:
            return 0
        else:
            self.image = pygame.image.load("laser.png")
            self.rect = self.image.get_rect()
            self.rect.center = (self.gs.player.rect.center)        
            self.sprites.append(self.rect)        
            self.images.append(self.image)
        #print(len(self.sprites))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = pygame.image.load("globe.png")
        self.rect = self.image.get_rect()
        self.rect.center = (600,500)
        self.health = 500

    def tick(self):
        if not self.rect.collidelist(self.gs.laser.sprites):
            self.health-=1
        
        
        #print self.health

        if self.health < 30:
            self.image = pygame.image.load("globe_red100.png")
            self.rect = self.image.get_rect()
            self.rect.center = (600,500)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs

    def tick(self):
        print("explosion")
        #explosion sequence

class GameSpace:
    def main(self):
        pygame.init()
    
        self.size = self.width, self.height = 640, 480
        self.black = 0,0,0

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()
        self.player = Player(self)    
        self.enemy = Enemy(self)
        self.laser = Laser(self)

        while 1:
            self.clock.tick(60)
            
            self.player.tick()
            self.enemy.tick()
            self.laser.tick()                    
            self.enemy.tick()

            self.screen.fill(self.black)
            for i in range(len(self.laser.sprites)):
                self.screen.blit(self.laser.images[i],self.laser.sprites[i])
            self.screen.blit(self.player.image,self.player.rect)
            self.screen.blit(self.enemy.image,self.enemy.rect)
    
            pygame.display.flip()

            for event in pygame.event.get():
    
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.player.tofire = True
                    self.laser.firing = True
                elif event.type == MOUSEBUTTONUP:
                    self.laser.firing = False
                    self.player.tofire = False
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.player.move(0,2)
                    elif event.key == K_UP:
                        self.player.move(0,-2)
                    elif event.key == K_RIGHT:
                        self.player.move(2,0)
                    elif event.key == K_LEFT:
                        self.player.move(-2,0)        

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
