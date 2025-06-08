from gameobject import GameObject
from pathlib import Path
import pygame
import math
import random

#護盾類別
class Shield(GameObject):
    # 類別變數，用於儲存音效
    shield_sound = None
    shield_break_sound = None

    #建構式
    def __init__(self, playground, xy = None, sensitivity = 1, scale_factor = 0.05):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__shield_path = __parent_path /'assets' /'images' /'shield.png'
        self._image = pygame.image.load(self.__shield_path)

        # 載入護盾音效
        if Shield.shield_sound is None:
            sound_path = __parent_path / 'assets' / 'sound' / 'shield.wav'
            Shield.shield_sound = pygame.mixer.Sound(sound_path)
            Shield.shield_sound.set_volume(0.3)  # 設定音量為 30%
        
        # 載入護盾破壞音效
        if Shield.shield_break_sound is None:
            sound_path = __parent_path / 'assets' / 'sound' / 'shieldbreak.wav'
            Shield.shield_break_sound = pygame.mixer.Sound(sound_path)
            Shield.shield_break_sound.set_volume(0.3)  # 設定音量為 30%

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
            self._x = xy[0]
            self._y = xy[1]
        
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w, 
            self._image.get_rect().h
        )
        
        # 隨機初始水平速度方向
        self._vx = random.choice([-1, 1]) * 2
        self._vy = 1

        self._objectBound = (
            10, 
            self._playground[0] - (self._image.get_rect().w + 10), 
            10, 
            self._playground[1] - (self._image.get_rect().h + 10)
        )

    #只會往上，override parent's method
    def update(self):
        GameObject.update(self)
        self._y += self._vy
        self._x += self._vx

        if self._x <= self._objectBound[0]:
            self._x = self._objectBound[0]
            self._vx = -self._vx
        elif self._x >= self._objectBound[1]:
            self._x = self._objectBound[1]
            self._vx = -self._vx
        
        if self._y > self._objectBound[3]:
            self._available = False
        
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2