import pygame as pg
from object import ObjectStatic

class Collectible(ObjectStatic):
    def __init__(self, position, size, points=10):
        super().__init__(position, size)
        self.points = points
        self.collected = False
        
    def render(self, surface):
        if not self.collected:
            #Renderizar depois as ovelinhas
            center_x = int(self._position.x + self._size.x / 2)
            center_y = int(self._position.y + self._size.y / 2)
            radius = int(min(self._size.x, self._size.y) / 2)
            pg.draw.circle(surface, (255, 255, 0), (center_x, center_y), radius)
            pg.draw.circle(surface, (255, 215, 0), (center_x, center_y), radius - 2)
    
    def collect(self):
        self.collected = True
        return self.points
    
    def is_collected(self):
        return self.collected
