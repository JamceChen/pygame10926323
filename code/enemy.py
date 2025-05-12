from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from gameobject import GameObject
import math

class Enemy(GameObject):
    # 建構式， playground為必要參數
    def __init__(self, playground, xy=None, sensitivity=1, scale_factor=0.2):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path/'assets'/'images'/'enemy.png'
        self._image = pygame.image.load(self.__enemy_path)
        
        original_width = self._image.get_rect().width
        original_height = self._image.get_rect().height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # 縮放圖片
        self._image = pygame.transform.smoothscale(self._image, (new_width, new_height))
        self._image = pygame.transform.flip(self._image, False, True)  # 垂直翻轉（180 度）

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2  # 水平置中
            self._y = -self._image.get_rect().h - 10 # 在畫面上方之外
        else:
            self._x = xy[0]
            self._y = xy[1]
            
        self._vx = 1  # 水平速度，每次 update 移動 3 像素
        self._vy = 1  # 垂直速度，每次 update 向下移動 1 像素
        
        # 更新中心點及碰撞半徑
        self._center = (self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2)
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)
        
        # 設定物件邊界
        self._objectBound = (
            0,  # 左邊界
            self._playground[0] - self._image.get_rect().w,  # 右邊界
            0,  # 上邊界
            self._playground[1] - self._image.get_rect().h  # 下邊界
        )
        
        # 初始化碰撞狀態
        self._collided = False
        self._hp = 100  # 添加生命值
        self.availble = True  # 設定為可用

    def update(self):
        GameObject.update(self)
        # 自己往下移動
        self._y += self._vy

        # 左右自動移動
        self._x += self._vx

        # 邊界檢查與反彈
        if self._x <= self._objectBound[0]:  # 碰到左邊界
            self._x = self._objectBound[0]  # 修正位置，避免卡在邊界外
            self._vx = -self._vx  # 水平反彈
        elif self._x >= self._objectBound[1]:  # 碰到右邊界
            self._x = self._objectBound[1]  # 修正位置，避免卡在邊界外
            self._vx = -self._vx  # 水平反彈
            
        # 如果敵人超出下邊界，設為不可用
        if self._y > self._objectBound[3]:
            self.availble = False

        # 更新中心點
        self._center = (self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2)
    
    def collision_detect(self, other_object):
        """檢測與其他物件的碰撞"""
        if not self.availble or not other_object.availble:
            return False
            
        dx = self._center[0] - other_object._center[0]
        dy = self._center[1] - other_object._center[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < (self._radius + other_object._radius):
            self._collided = True
            return True
        return False
        
    def take_damage(self, damage=10):
        """受到傷害，減少生命值"""
        self._hp -= damage
        if self._hp <= 0:
            self.availble = False
        return self._hp <= 0  # 回傳是否已經死亡
    
    # 以下是獲取屬性的方法，讓外部可以安全訪問私有屬性
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
        
    @property
    def center(self):
        return self._center
        
    @property
    def radius(self):
        return self._radius
        
    @property
    def hp(self):
        return self._hp