#資源呼叫

from pathlib import Path
import pygame

#戰鬥機圖片
def load_plane_image():
    plane_path = Path(__file__).parent.parent / 'assets' / 'images' / '6.png'
    return pygame.image.load(str(plane_path)).convert_alpha()

#icon
def load_icon_image():
    icon_path = Path(__file__).parent.parent/ 'assets' / 'images' / 'icon.png'
    return pygame.image.load(str(icon_path))
