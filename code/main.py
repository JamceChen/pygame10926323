import pygame
import config #參數位置
import resources #資源呼叫(圖片、音效)
from pathlib import Path
import math
from gameobject import GameObject
from player import Player


    
#初始化pygame 系統
pygame.init()

#建立視窗物件的寬跟高
playground = [config.screenWidth,config.screenHigh]
screen = pygame.display.set_mode((config.screenWidth,config.screenHigh))

clock = pygame.time.Clock()
player = Player(playground=playground, senitivity=config.movingScale)
#tilte
pygame.display.set_caption(config.window_title)

#icon圖片
pygame.display.set_icon(resources.load_icon_image())

#視窗背景
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100,100,100))

keyCountX = 0
keyCountY = 0
#設定迴圈讓視窗保持更新
while config.running:
    #從pygame事件佇列中一項項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                keyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_s:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_w:
                keyCountY += 1
                player.to_the_top()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1
        
    screen.blit(background,(0,0))
    player.update()
    screen.blit(player._image, (player.x, player.y))
    #更新螢幕狀態
    pygame.display.update()

    #每秒更新fps次
    dt = clock.tick(config.fps)

#關閉視窗
pygame.quit()