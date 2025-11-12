import pygame

class SecretArea:
    def __init__(self, x, y, width, height, color_hex):
        """
        Cria uma área secreta que se torna invisível quando o player está dentro dela
        
        Args:
            x (int): Posição X do retângulo
            y (int): Posição Y do retângulo  
            width (int): Largura do retângulo
            height (int): Altura do retângulo
            color_hex (str): Cor em formato hexadecimal (ex: "#FF0000")
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = self._hex_to_rgb(color_hex)
        self.is_visible = True  # Controla se a área está visível
        self.alpha = 255  # Transparência (0-255)
        
    def _hex_to_rgb(self, hex_color):
        """Converte cor hexadecimal para RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def check_player_collision(self, player_rect):
        """
        Verifica se pelo menos metade do player está dentro da área secreta
        
        Args:
            player_rect (pygame.Rect): Retângulo do player
            
        Returns:
            bool: True se metade ou mais do player está dentro da área
        """
        # Calcular a área de intersecção
        intersection = self.rect.clip(player_rect)
        
        if intersection.width <= 0 or intersection.height <= 0:
            return False
            
        # Calcular área do player e área de intersecção
        player_area = player_rect.width * player_rect.height
        intersection_area = intersection.width * intersection.height
        
        # Verificar se pelo menos 50% do player está dentro da área
        return intersection_area >= (player_area * 0.5)
    
    def update(self, player_rect):
        """
        Atualiza a visibilidade da área baseada na posição do player
        
        Args:
            player_rect (pygame.Rect): Retângulo do player
        """
        should_be_invisible = self.check_player_collision(player_rect)
        
        if should_be_invisible and self.is_visible:
            # Player entrou na área - começar a ficar invisível
            self.is_visible = False
            self.alpha = max(0, self.alpha - 15)  # Fade out gradual
        elif not should_be_invisible and not self.is_visible:
            # Player saiu da área - começar a ficar visível
            self.is_visible = True
            self.alpha = min(255, self.alpha + 15)  # Fade in gradual
        
        # Ajustar alpha gradualmente
        if not self.is_visible:
            self.alpha = max(0, self.alpha - 10)
        else:
            self.alpha = min(255, self.alpha + 10)
    
    def render(self, surface):
        """
        Renderiza a área secreta com transparência
        
        Args:
            surface (pygame.Surface): Superfície onde desenhar
        """
        if self.alpha > 0:
            # Criar uma superfície temporária com transparência
            temp_surface = pygame.Surface((self.rect.width, self.rect.height))
            temp_surface.set_alpha(self.alpha)
            temp_surface.fill(self.color)
            
            # Desenhar na superfície principal
            surface.blit(temp_surface, (self.rect.x, self.rect.y))
    
    def get_info(self):
        """Retorna informações da área secreta para debug"""
        return {
            'position': (self.rect.x, self.rect.y),
            'size': (self.rect.width, self.rect.height),
            'color': self.color,
            'visible': self.is_visible,
            'alpha': self.alpha
        }