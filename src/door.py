import pygame
from Object import ObjectStatic

class Door(ObjectStatic):
    def __init__(self, position, size, closed_image, open_image):
        super().__init__(position, size)
        self.closed_image = closed_image
        self.open_image = open_image
        self.is_open = False

    def open_door(self):
        """Abre a porta quando o jogador tem a chave"""
        self.is_open = True

    def close_door(self):
        """Fecha a porta (para reset do jogo)"""
        self.is_open = False

    def render(self, screen):
        pos = self.get_position()
        
        # Escolhe a imagem baseada no estado da porta
        current_image = self.open_image if self.is_open else self.closed_image
        
        if current_image:
            screen.blit(current_image, (int(pos.x), int(pos.y)))
        else:
            # Fallback caso não tenha imagem
            size = self.get_size()
            center = pos + (size / 2.0)
            rect = pygame.Rect(
                int(center.x - size.x / 2),
                int(center.y - size.y / 2),
                int(size.x),
                int(size.y)
            )
            color = (0, 255, 0) if self.is_open else (139, 69, 19)  # Verde se aberta, marrom se fechada
            pygame.draw.rect(screen, color, rect)

    def get_is_open(self):
        return self.is_open
