import pygame,sys #sys是python的标准库，提供Python运行时环境变量的操控
from pygame.locals import *

from game import *
from const import *

pygame.init()  #内部各功能模块进行初始化创建及变量设置，默认调用
size = width,height = GAME_W*BLOCK_SIZE+30,GAME_H*BLOCK_SIZE+105  #设置游戏窗口大小，分别是宽度和高度
SUR_SCREEN = pygame.display.set_mode(size)  #初始化显示窗口
pygame.display.set_caption("MineSweeper by --AZGC--")  #设置显示窗口的标题内容，是一个字符串类型
icon = pygame.image.load("pic/icon.ico")
pygame.display.set_icon(icon)

game = Game(SUR_SCREEN)
while True:  #无限循环，直到Python运行时退出结束
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():  #从Pygame的事件队列中取出事件，并从队列中删除该事件
        if event.type == pygame.QUIT:  #获得事件类型，并逐类响应
            pygame.quit()
            sys.exit()   #用于退出结束游戏并退出

    game.update()#类似gms的step
    game.draw()#类似gms的draw

    pygame.display.update()  #对显示窗口进行更新，默认窗口全部重绘