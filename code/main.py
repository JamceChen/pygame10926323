import pygame
import config #參數位置
import resources #資源呼叫(圖片、音效)
from pathlib import Path
import math
from gameobject import GameObject
from player import Player
from mymissile import MyMissile
from enemy import Enemy
    
#初始化pygame 系統
pygame.init()

#建立視窗物件的寬跟高
playground = [config.screenWidth,config.screenHigh]
screen = pygame.display.set_mode((config.screenWidth,config.screenHigh))

clock = pygame.time.Clock()
player = Player(playground=playground, sensitivity=config.movingScale)
enemy = Enemy(playground=playground, sensitivity=config.movingScale)
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

#建立物件串列
Missiles = []
enemys = []

#建立事件編號
launchMissile = pygame.USEREVENT + 1

#設定迴圈讓視窗保持更新
while config.running:
    #從pygame事件佇列中一項項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.running = False

        if event.type == launchMissile:
            m_x = player._x - 50
            m_y = player._y
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground,sensitivity=config.movingScale))
            m_x = player._x + 40
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground,sensitivity=config.movingScale))

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

            if event.key == pygame.K_SPACE:
                m_x = player._x - 50
                m_y = player._y
                Missiles.append(MyMissile(xy = (m_x,m_y),playground=playground, sensitivity=config.movingScale))
                m_x = player.x + 40
                Missiles.append(MyMissile(playground, (m_x,m_y),config.movingScale)) #若未指定參數需按照宣告順序
                pygame.time.set_timer(launchMissile,400) #之後每400ms發射一組

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

            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0) #停止發射
        
    screen.blit(background,(0,0))
    Missiles = [item for item in Missiles if item._availble]
    for m in Missiles:
        m.update()
        screen.blit(m._image,(m.x+3, m.y))

    enemys= [item for item in enemys  if item._availble]
    for m in enemys:
        m.update()
        screen.blit(m._image,(m.x+3, m.y))
    enemy.update()
    screen.blit(enemy._image, (enemy.x, enemy.y))
    player.update()
    screen.blit(player._image, (player.x, player.y))
    #更新螢幕狀態
    pygame.display.update()

    #每秒更新fps次
    dt = clock.tick(config.fps) 

#關閉視窗
pygame.quit()