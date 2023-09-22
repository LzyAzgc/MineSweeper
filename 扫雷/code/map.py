import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *

from const import *
from block import *

import math

class Map():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.MAP = []#创建map
        for x in range(self.width):#初始化map
            row = []
            for y in range(self.height):
                obj = Block(ALL_IMAGES[Image.block][0],self.x+x*32,self.y+y*32,32,32)
                row.append(obj)#加入obj
            self.MAP.append(row)

    def update(self):
        for x in range(self.width):
            for y in range(self.height):
                obj = self.MAP[x][y]
                obj.moveto(self.x+x*32,self.y+y*32)
    
    def draw(self,surface):#绘制map
        for x in range(self.width):
            for y in range(self.height):
                obj = self.MAP[x][y]
                obj.draw(surface)

    def add(self,image,row,col):
        x = row % self.width
        y = col % self.height
        self.MAP[x][y].imageSet(image)

    def clear(self,image):
        for x in range(self.width):
            for y in range(self.height):
                self.MAP[x][y].imageSet(image)
    
    def getMap(self):
        return self.MAP
    
    def getObj(self,row,col):
        x = row % self.width
        y = col % self.height
        return self.MAP[x][y]
    
    def getRoundRowColIdx(self,x,y):
        row = math.floor((x-self.x)/32)
        col = math.floor((y-self.y)/32)
        return (row,col)

                

