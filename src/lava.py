import pygame
from object import ObjectStatic
from animated_gif import AnimatedGif

class Lava(ObjectStatic):
    def __init__(self, position, size, image=None, animated_gif=None):
        super().__init__(position, size)
        self.image = image
        self.animated_gif = animated_gif
        
    def update(self, delta_time_ms=16.67):
        if self.animated_gif:
            self.animated_gif.update(delta_time_ms)

    def render(self, screen):
        pos = self.get_position()
        
        # Use animated gif if available
        if self.animated_gif:
            current_frame = self.animated_gif.get_current_frame()
            if current_frame:
                screen.blit(current_frame, (int(pos.x), int(pos.y)))
                return
                
        # Fallback to static image
        if self.image:
            screen.blit(self.image, (int(pos.x), int(pos.y)))
        else:
            # Fallback to colored rectangle
            size = self.get_size()
            center = pos + (size / 2.0)
            rect = pygame.Rect(
                int(center.x - size.x / 2),
                int(center.y - size.y / 2),
                int(size.x),
                int(size.y)
            )
            pygame.draw.rect(screen, (255, 50, 0), rect)  # Orange-red for lava
    
