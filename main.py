import pygame
#初始化pygame 系統
pygame.init()
#建立視窗物件的寬跟高
screenHigh = 760
screenWidth = 1000
playground = [screenWidth,screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))

running = True
#更新頻率
fps = 120
clock = pygame.time.Clock()
#設定迴圈讓視窗保持更新
while running:
    #從pygame事件佇列中一項項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新螢幕狀態
    pygame.display.update()
    #每秒更新fps次
    dt = clock.tick(fps)
#關閉視窗
pygame.quit()