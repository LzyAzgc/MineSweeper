import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *
import os

from const import *
from map   import *
from object import *
from utils import *

import random
import math

#-------------------游戏主体---------------------#

class Game():
    def __init__(self,gameSurface):#初始化
        self.gameSurface = gameSurface#所选画布
        self.Game_W = GAME_W
        self.Game_H = GAME_H
        self.Game_Mines_Num = GAME_MINES_NUM
        self.restGame()

    def update(self):#step----------------------------------------------------
        mouse_presses = pygame.mouse.get_pressed()
        pressed = pygame.key.get_pressed()
        
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        (row,col) = self.MAP.getRoundRowColIdx(mx,my)#get 鼠标在雷盘里的位置
        fx = self.FACE.x
        fy = self.FACE.y
        isRest = (mx >= fx) & (my >= fy) & (mx <= fx+48) & (my <= fy+48)
        if mouse_presses[0]:#按下鼠标左
            if self.m_p1 == 1:
                if isRest:
                    self.FACE.imageSet(ALL_IMAGES[Image.face][1+(self.GameOver==2)*3+(self.GameOver==1)*5])
                if self.GameOver == 0:
                    self.openBlock(row,col)#打开
                self.m_p1 = 0
        else:
            self.FACE.imageSet(ALL_IMAGES[Image.face][(self.GameOver==2)*3+(self.GameOver==1)*5])
            if self.m_p1 == 0:
                if isRest:
                    self.restGame()
                self.m_p1 = 1

        if mouse_presses[2]:#按下鼠标右
            if self.m_p2 == 1:
                if self.GameOver == 0:
                    self.setFlag(row,col)#插旗
                self.m_p2 = 0
        else:
            if self.m_p2 == 0:

                self.m_p2 = 1
        if pressed[K_r]:#方便重启
            self.restGame()
            
    def draw(self):#draw---------------------------------------------------------------
        self.gameSurface.fill((192,192,192))#刷新屏幕，准备渲染
        w = self.gameSurface.get_width()
        self.drawLineBlk((w-32*self.Game_W)//2,90,self.Game_W*32,self.Game_H*32,self.gameSurface)
        self.drawLineBlk(15,15,w-30,60,self.gameSurface)
        self.MAP.draw(self.gameSurface)
        self.FACE.draw(self.gameSurface)
        self.drawNum(self.Game_Mines_Num-len(self.flags),22,22,3,self.gameSurface)
        if self.GameOver == 0:
            if self.mines != []:
                self.partTime = math.floor(self.TIME.getPartTime())
            else:
                self.partTime = 0
        self.drawNum(self.partTime,w-100,22,3,self.gameSurface)
        
    #--------------------------------------------非主体函数-----------------------------------------------
    def init(self):
        self.GameOver = 0
        if self.Game_W < 2:
            self.Game_W = 2
        if self.Game_H < 2:
            self.Game_H = 2
        if self.Game_Mines_Num < 1:
            self.Game_Mines_Num = 1
        if self.Game_Mines_Num >= self.Game_W*self.Game_H:
            self.Game_Mines_Num = self.Game_W*self.Game_H-1
        self.MAP = Map((self.gameSurface.get_width()-32*self.Game_W)//2,90,self.Game_W,self.Game_H)
        self.FACE = Object(ALL_IMAGES[Image.face][0],self.gameSurface.get_width()//2-24,20,48,48)
        self.TIME = Time()

        self.partTime = 0
        self.mines = []
        self.flags = []
        self.poses = []
        for x in range(self.Game_W):
            for y in range(self.Game_H):
                self.poses.append((x,y))

        self.m_p1 = 1
        self.m_p2 = 1

    def openBlock(self,row,col):
        isOpen = 1
        if row < 0:#防出圈
            isOpen = 0
        if row >= self.Game_W:
            isOpen = 0
        if col < 0:
            isOpen = 0
        if col >= self.Game_H:
            isOpen = 0

        if isOpen:
            pos = (row,col)
            obj = self.MAP.getObj(row,col)
            if obj.image == ALL_IMAGES[Image.block][0]:#如果是关的，那打开
                self.FACE.imageSet(ALL_IMAGES[Image.face][2])
                if pos in self.mines:#扫到雷时
                    self.gameOver()
                    self.MAP.add(ALL_IMAGES[Image.mine][1],row,col)
                else:
                    self.poses.remove(pos)
                    if len(self.poses) == self.Game_W*self.Game_H-1:
                        self.putMines(self.Game_Mines_Num)#开局防雷措施
                        self.TIME.setCreateTime()
                    if len(self.poses) == 0:
                        self.gameWin()
                    num = self.countMines(row,col)#数一数周围的雷
                    self.MAP.add(ALL_IMAGES[Image.blkNum][num],row,col)
                    if num == 0:#空白时翻开全部
                        for x in range(3):
                            for y in range(3):
                                self.openBlock(row-1+x,col-1+y)

    def drawNum(self,num,x,y,length,surface):
        self.num = str(num)
        self.num = abs(length-len(self.num))*"0"+self.num
        for i in range(length):
            self.img = ALL_IMAGES[Image.timeNum][int(self.num[i])]
            self.img = pygame.transform.scale(self.img,(26,46))
            surface.blit(self.img,(x+i*26,y))

    def setFlag(self,row,col):#插旗
        isSet = 1
        if row < 0:#防出圈
            isSet = 0
        if row >= self.Game_W:
            isSet = 0
        if col < 0:
            isSet = 0
        if col >= self.Game_H:
            isSet = 0

        if isSet:
            obj = self.MAP.getObj(row,col)
            leftFlagNum = self.Game_Mines_Num-len(self.flags)#插
            if (obj.image == ALL_IMAGES[Image.block][0]) & (leftFlagNum > 0):
                self.MAP.add(ALL_IMAGES[Image.block][2],row,col)
                self.flags.append((row,col))
                if leftFlagNum == 1:#检测是否插满所有雷
                    for flg in self.flags:
                        if flg not in self.mines:
                            return 0
                    self.gameWin()
            elif obj.image == ALL_IMAGES[Image.block][2]:#取消
                self.MAP.add(ALL_IMAGES[Image.block][0],row,col)
                self.flags.remove((row,col))
            

    def gameOver(self):
        self.GameOver = 1
        for mine in self.mines:#其他雷显示
            row = mine[0]
            col = mine[1]
            self.MAP.add(ALL_IMAGES[Image.mine][0],row,col)

    def gameWin(self):
        self.GameOver = 2
        for mine in self.mines:#其他雷显示
            row = mine[0]
            col = mine[1]
            self.MAP.add(ALL_IMAGES[Image.block][2],row,col)

    def countMines(self,row,col):#数雷
        num =  0
        for x in range(3):
            for y in range(3):
                pos = (row-1+x,col-1+y)
                if pos in self.mines:
                    num+=1
        return num

    def putMines(self,num):#布雷
        for i in range(num):
            cp = random.choice(self.poses)
            self.mines.append(cp)
            self.poses.remove(cp)
    
    def restGame(self):
        f = open('data.txt','r')
        data = f.readlines()
        f.close()
        self.Game_W = int(data[0])
        self.Game_H = int(data[1])
        self.Game_Mines_Num = int(data[2])
        width,hieght  = self.Game_W*BLOCK_SIZE+30,self.Game_H*BLOCK_SIZE+105  #设置游戏窗口大小，分别是宽度和高度
        if width<274:
            width = 274
        if hieght<169:
            hieght = 169
        ww = pygame.display.Info().current_w//2
        wh = pygame.display.Info().current_h//2
        self.gameSurface = pygame.display.set_mode((width,hieght))
        os.environ['SDL_VIDEO_WINDOW_POS'] = str((ww-self.Game_W//2, wh-self.Game_H//2))

        self.init()

    def drawLineBlk(self,x,y,w,h,surface):
        self.surface = surface

        lu = pygame.transform.scale(ALL_IMAGES[Image.lineblk][2],(w+4,h+4))
        rd = pygame.transform.scale(ALL_IMAGES[Image.lineblk][3],(w+4,h+4))
        lur = lu.get_rect()
        lur.left = x-4
        lur.top = y-4
        rdr = lu.get_rect()
        rdr.left = x
        rdr.top = y
        self.surface.blit(lu,lur)
        self.surface.blit(rd,rdr)
        
        lu = pygame.transform.scale(ALL_IMAGES[Image.lineblk][1],(4,4))
        rd = pygame.transform.scale(ALL_IMAGES[Image.lineblk][1],(4,4))
        lur = lu.get_rect()
        lur.right = x
        lur.top = y+h
        rdr = rd.get_rect()
        rdr.left = x+w
        rdr.bottom = y
        self.surface.blit(lu,lur)
        self.surface.blit(rd,rdr)
        pygame.draw.rect(self.surface,(192,192,192),[x,y,w,h],0)
