import pygame as pg
from Object import ObjectStatic
import os
from animated_gif import AnimatedGif

class CollectibleType:
    BLACK_SHEEP = "black_sheep"
    WHITE_SHEEP = "white_sheep"

class Collectible(ObjectStatic):
    def __init__(self, position, size, collectible_type, points=10):
        super().__init__(position, size)
        self.points = points
        self.collected = False
        self.collectible_type = collectible_type
        self.animated_sprite = self._load_animated_sprite()
        
    def _load_animated_sprite(self):
        base_path = os.path.dirname(__file__)
        sprite_path = os.path.join(base_path, '..', 'resources', 'collectible', f'{self.collectible_type}.gif')
        animated_gif = AnimatedGif(sprite_path, (int(self._size.x), int(self._size.y)))
        return animated_gif
  
        
    def render(self, surface):
        if not self.collected:
            if self.animated_sprite:
                self.animated_sprite.update()
                current_frame = self.animated_sprite.get_current_frame()
                if current_frame:
                    surface.blit(current_frame, self._position)
                else:
                    self._render_fallback(surface)
            else:
                self._render_fallback(surface)
    
    def _render_fallback(self, surface):
        center_x = int(self._position.x + self._size.x / 2)
        center_y = int(self._position.y + self._size.y / 2)
        radius = int(min(self._size.x, self._size.y) / 2)
        
        if self.collectible_type == CollectibleType.BLACK_SHEEP:
            color = (50, 50, 50)
        elif self.collectible_type == CollectibleType.WHITE_SHEEP:
            color = (255, 255, 255)
        else:
            color = (255, 255, 0)
            
        pg.draw.circle(surface, color, (center_x, center_y), radius)
        pg.draw.circle(surface, (0, 0, 0), (center_x, center_y), radius, 2) 
    
    def collect(self):
        self.collected = True
        return self.points
    
    def is_collected(self):
        return self.collected
    
    def get_type(self):
        return self.collectible_type
    
    def reset_animation(self):
        if self.animated_sprite:
            self.animated_sprite.reset()
