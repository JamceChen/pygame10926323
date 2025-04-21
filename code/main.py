import pygame
from pathlib import Path

#初始化pygame 系統
pygame.init()

#建立視窗物件的寬跟高
screenHigh = 760
screenWidth = 1000
playground = [screenWidth,screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))

#設定迴圈變數
running = True

#更新頻率
fps = 120
clock = pygame.time.Clock()

#tilte
pygame.display.set_caption("戰鬥機遊戲")

#戰鬥機圖片
plane_path = Path(__file__).parent.parent/'picture'/'myplane.png'
plane_img = pygame.image.load(str(plane_path)).convert_alpha()
#icon圖片
icon_path = Path(__file__).parent.parent/'picture'/'icon.png'
icon_img = pygame.image.load(icon_path)
pygame.display.set_icon(icon_img)
#視窗背景
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,250,250))
#設定迴圈讓視窗保持更新
while running:
    #從pygame事件佇列中一項項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background,(0,0))
    screen.blit(plane_img, (100, 100))
    #更新螢幕狀態
    pygame.display.update()

    #每秒更新fps次
    dt = clock.tick(fps)

#關閉視窗
pygame.quit()