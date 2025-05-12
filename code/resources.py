#資源呼叫

from pathlib import Path
import pygame

#icon
def load_icon_image():
    icon_path = Path(__file__).parent.parent/ 'assets' / 'images' / 'icon.png'
    return pygame.image.load(str(icon_path))

