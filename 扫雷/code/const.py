import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *

#----------------------常量初始化------------------------#

f = open('data.txt','r')
data = f.readlines()
f.close()

GAME_W = int(data[0])#长宽
GAME_H = int(data[1])
GAME_MINES_NUM = int(data[2])
GAME_SPEED = 60#帧率

BLOCK_SIZE = 32#方块大小
BLOCK_DROPSPEED = 50#

GAME_OVER = 0

class Image():
    block = 0
    blkNum  = 1
    mine = 2
    timeNum = 3
    face = 4
    lineblk = 5

IMAGEAll = pygame.image.load('pic/all.png')

#13,23
#24,24
#16,16

# 0
# 24
# 49
# 66

ALL_IMAGES = {
    Image.block : [IMAGEAll.subsurface(pygame.Rect(17*i,49,16,16)) for i in range(3)],
    Image.blkNum : [IMAGEAll.subsurface(pygame.Rect(17*i,66,16,16)) for i in range(9)],
    Image.mine : [IMAGEAll.subsurface(pygame.Rect(17*(i+5),49,16,16)) for i in range(3)],
    Image.timeNum : [IMAGEAll.subsurface(pygame.Rect(14*i,0,13,23)) for i in range(10)],
    Image.face : [IMAGEAll.subsurface(pygame.Rect(25*i,24,24,24)) for i in range(7)],
    Image.lineblk : [IMAGEAll.subsurface(pygame.Rect(136+3*i,49,2,2)) for i in range(4)],
}

GAME_INPUT = {
    'UP' : K_UP,
    'DOWN' : K_DOWN,
    'LEFT' : K_LEFT,
    'RIGHT' : K_RIGHT,
}
