from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from gameobject import GameObject
from shield import Shield
from rock import Rock
import math

#玩家類別
class Player(GameObject):
    #建構式，playground 為必要參數
    def __init__(self, playground, xy = None, sensitivity = 1, scale_factor = 0.3):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path /'assets' /'images' /'airforce.png'
        self._image = pygame.image.load(self.__player_path)

        # 縮放圖片
        original_width = self._image.get_rect().width
        original_height = self._image.get_rect().height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self._image = pygame.transform.smoothscale(
            self._image, 
            (new_width, new_height)
        )

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w)/2
            self._y = 3 * self._playground[1]/4
        
        else:
            self._x = xy[0]#貼圖位置
            self._y = xy[1]
        
        self._hp = 100
        self._score = 0  # 新增分數屬性
        self._has_shield = False  # 新增護盾狀態
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w, 
            self._image.get_rect().h
        ) #碰撞半徑

        self._objectBound = (
            10, 
            self._playground[0] - (self._image.get_rect().w + 10), 
            10, 
            self._playground[1] - (self._image.get_rect().h + 10)
        )
    
    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
    
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                if isinstance(m, Shield):  # 如果是護盾
                    self._has_shield = True
                    m._available = False
                    m._collided = True
                    Shield.shield_sound.play()  # 播放獲得護盾音效
                elif isinstance(m, Rock):  # 如果是石頭
                    if self._has_shield:
                        self._has_shield = False
                        Shield.shield_break_sound.play()  # 播放護盾破壞音效
                    else:
                        self._hp -= 20
                    m._available = False
                    m._collided = True
                else:  # 如果是普通敵人
                    if self._has_shield:
                        self._has_shield = False
                        Shield.shield_break_sound.play()  # 播放護盾破壞音效
                    else:
                        self._hp -= 10
                    m._available = False
                    m._collided = True