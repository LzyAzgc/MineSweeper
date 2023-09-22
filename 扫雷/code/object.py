import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *

from const import *

class Object():
    def __init__(self,image,x,y,w,h):
        self.image = image
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def draw(self,surface):
        img = pygame.transform.scale(self.image,(self.w,self.h))
        surface.blit(img, self.rect)
    
    def moveto(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def imageSet(self,image):
        self.image = image

    def sizeSet(self,w,h):
        self.w = w
        self.h = h