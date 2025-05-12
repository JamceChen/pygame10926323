import pygame
import config #參數位置
import resources #資源呼叫(圖片、音效)
from pathlib import Path
import math
import random
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
enemies = []  

#建立事件編號
launchMissile = pygame.USEREVENT + 1
spawnEnemy = pygame.USEREVENT + 100  # 新增敵人生成事件

# 設定敵人產生計時器，每1.5秒產生一個敵人
pygame.time.set_timer(spawnEnemy, 150)

# 分數
score = 0
font = pygame.font.SysFont(None, 36)

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

        if event.type == spawnEnemy:
            # 產生敵人在隨機的x位置
            enemy_x = random.randint(0, config.screenWidth - 50)  # 假設敵人寬度約50
            enemies.append(Enemy(playground=playground, xy=(enemy_x, -50), sensitivity=config.movingScale))

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
                m_x = player._x + 40  # 修正: player.x -> player._x
                Missiles.append(MyMissile(playground=playground, xy=(m_x,m_y), sensitivity=config.movingScale))  # 修正參數順序和命名
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
    
    # 更新玩家
    player.update()
    
    # 更新並檢查子彈邊界，移除超出邊界的子彈
    available_missiles = []
    for missile in Missiles:
        missile.update()
        if missile._availble:  # 檢查子彈是否仍然可用
            available_missiles.append(missile)
    Missiles = available_missiles
    
    # 更新並檢查敵人
    available_enemies = []
    for enemy in enemies:
        enemy.update()
        
        # 檢查敵人是否碰到底部邊界
        if enemy._y > config.screenHigh:
            enemy.availble = False 
        
        # 檢查敵人與玩家碰撞
        dx = enemy._center[0] - player._center[0]
        dy = enemy._center[1] - player._center[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < (enemy._radius + player._radius):
            enemy.availble = False
            player._hp -= 1  # 玩家受傷
            if player._hp <= 0:
                gameover_path = Path(__file__).parents[1]/'assets'/'images'/'gameover.png'
                over_image = pygame.image.load(gameover_path)
                screen.blit(over_image, (0, 0))
                
        
        # 檢查敵人與子彈碰撞
        for missile in Missiles:
            dx = enemy._center[0] - missile._center[0]
            dy = enemy._center[1] - missile._center[1]
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < (enemy._radius + missile._radius):
                enemy.availble = False
                missile._availble = False
                score += 100  # 擊中敵人加分
                break
        
        if enemy.availble:  # 如果敵人仍然可用，保留在列表中
            available_enemies.append(enemy)
    
    enemies = available_enemies  # 更新敵人列表
    
    # 繪製畫面
    screen.blit(background,(0,0))
    
    # 繪製分數
    #score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    #screen.blit(score_text, (10, 10))
    
    # 繪製玩家生命值
    #hp_text = font.render(f"HP: {player._hp}", True, (255, 255, 255))
    #screen.blit(hp_text, (10, 50))
    
    # 繪製子彈
    for missile in Missiles:
        screen.blit(missile._image, (missile._x, missile._y))
    
    # 繪製敵人
    for enemy in enemies:
        screen.blit(enemy._image, (enemy._x, enemy._y))
    
    # 繪製玩家
    screen.blit(player._image, (player._x, player._y))
    
    # 更新螢幕狀態
    pygame.display.update()

    # 每秒更新fps次
    dt = clock.tick(config.fps) 

# 關閉視窗
pygame.quit()