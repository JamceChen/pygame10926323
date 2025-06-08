from gameobject import GameObject
from pathlib import Path
import pygame

#飛彈類別
class MyMissile(GameObject):
    # 類別變數，用於儲存音效
    shoot_sound = None

    #建構式
    def __init__(self, playground, xy, sensitivity = 1, scale_factor = 0.2):
        GameObject.__init__(self, playground)
        __parent_path = Path(__file__).parents[1]
        self.__missile_path = __parent_path /'assets' /'images' /'missile.png'
        self._image = pygame.image.load(self.__missile_path)

        # 載入射擊音效
        if MyMissile.shoot_sound is None:
            sound_path = __parent_path / 'assets' / 'sound' / 'shoot.wav'
            MyMissile.shoot_sound = pygame.mixer.Sound(sound_path)
            MyMissile.shoot_sound.set_volume(0.3)  # 設定音量為 30%
        MyMissile.shoot_sound.play()

        # 縮放圖片
        original_width = self._image.get_rect().width
        original_height = self._image.get_rect().height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self._image = pygame.transform.smoothscale(
            self._image, 
            (new_width, new_height)
        )

        self._x = xy[0]
        self._y = xy[1]
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = self._image.get_rect().w/4
        

        #左右邊界不重要，上邊界等整個飛彈離開螢幕時觸發
        self._objectBound = (
            0, 
            self._playground[0], 
            -self._image.get_rect().h - 10, 
            self._playground[1]
        ) #右，左，上，下
        
        self._moveScale = 0.7 * sensitivity
        self.to_the_top() #設定移動方向

    #只會往上，override parent's method
    def update(self):
        self._y += self._changeY
        if self._y < self._objectBound[2]:
            #超過螢幕範圍，標記為無效
            self._available = False
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().w/2
    
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._collided = True
                self._available = False
                m._available = False