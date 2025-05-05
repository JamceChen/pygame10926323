from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from gameobject import GameObject
import math

class Player(GameObject):
    #建構式， playground為必要參數
    def __init__(self, playground, xy = None, senitivity = 1, scale_factor = 0.3):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * senitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path/'assets'/'images'/'airforce.png'
        self._image = pygame.image.load(self.__player_path)
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)

        original_width = self._image.get_rect().width
        original_height = self._image.get_rect().height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # 縮放圖片
        self._image = pygame.transform.scale(self._image, (new_width, new_height))
        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w)/2
            self._y = 3 * self._playground[1]/4
        else:
            self._x = xy[0]
            self._y = xy[1]

            self._objectBound = (10, self._playground[0] - (self._image.get_rect().w+10),10,self._playground[1]-(self._image.get_rect().h+10))

    

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w/2,self._y + self._image.get_rect().h/2
    
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                m.hp = -1
                m.collided = True
                m.available = False
    
    
