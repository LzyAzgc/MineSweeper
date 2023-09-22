import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *

from const import *
from object import *

class Block(Object):
    def __init__(self,image,x,y,w,h):
        super().__init__(image,x,y,w,h)
