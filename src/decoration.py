import pygame
from object import ObjectStatic

class Decoration(ObjectStatic):
    def __init__(self, position, size, image=None):
        super().__init__(position, size)
        self.image = image

    def render(self, screen):
        pos = self.get_position()

        if self.image:
            screen.blit(self.image, (int(pos.x), int(pos.y)))
        else:
            size = self.get_size()
            center = pos + (size / 2.0)
            rect = pygame.Rect(
                int(center.x - size.x / 2),
                int(center.y - size.y / 2),
                int(size.x),
                int(size.y)
            )
            pygame.draw.rect(screen, (30, 30, 30), rect) 

    def __del__(self):
        pass