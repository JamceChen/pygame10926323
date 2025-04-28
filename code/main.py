import pygame
import config #參數位置
import resources #資源呼叫(圖片、音效)
from pathlib import Path

#初始化pygame 系統
pygame.init()

#建立視窗物件的寬跟高
screen = pygame.display.set_mode((config.screenWidth,config.screenHigh))

clock = pygame.time.Clock()

#tilte
pygame.display.set_caption(config.window_title)
#戰鬥機圖片
plane_img = resources.load_plane_image()
#icon圖片
pygame.display.set_icon(resources.load_icon_image())

#視窗背景
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100,100,100))

#設定迴圈讓視窗保持更新
while config.running:
    #從pygame事件佇列中一項項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.running = False
    
    screen.blit(background,(0,0))
    screen.blit(plane_img, (100, 100))
    #更新螢幕狀態
    pygame.display.update()

    #每秒更新fps次
    dt = clock.tick(config.fps)

#關閉視窗
pygame.quit()