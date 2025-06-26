import pygame

from Object import ObjectStatic

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)


class Decoration(ObjectStatic):
    def __init__(self, position, size, image=None):
        super().__init__(position, size)
        self.image = image

    def render(self, screen):
        pos = self.get_position()

        if self.image:
            screen.blit(self.image, (int(pos.x), int(pos.y)))  # desenha a imagem
        else:
            size = self.get_size()
            center = pos + (size / 2.0)
            rect = pygame.Rect(
                int(center.x - size.x / 2),
                int(center.y - size.y / 2),
                int(size.x),
                int(size.y)
            )
            pygame.draw.rect(screen, (30, 30, 30), rect)  # fallback se não tiver imagem

    def __del__(self):
        pass