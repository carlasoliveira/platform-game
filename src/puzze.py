import pygame as pg
from object import ObjectDynamic
from constants import gravity
import os

class PuzzleType:
    MOVABLE_BLOCK = "movable_block"
    SWITCH = "switch" 
    DOOR = "door"
    PRESSURE_PLATE = "pressure_plate"

class Puzze(ObjectDynamic):
    def __init__(self, position, size, velocity, puzzle_type=PuzzleType.MOVABLE_BLOCK):
        super().__init__(position, size, velocity)
        self.m_puzzle_type = puzzle_type
        self.m_is_activated = False
        self.m_can_be_pushed = puzzle_type == PuzzleType.MOVABLE_BLOCK
        self.m_is_being_pushed = False
        self.m_push_resistance = 0.8
        self.m_image = None
        self._load_image()

    def _load_image(self):
        try:
            base_path = os.path.dirname(__file__)
            

            if self.m_puzzle_type == PuzzleType.MOVABLE_BLOCK:
                image_path = os.path.join(base_path, '..', 'resources', 'graphics', 'movable_block.png')
            elif self.m_puzzle_type == PuzzleType.SWITCH:
                image_path = os.path.join(base_path, '..', 'resources', 'graphics', 'switch.png')
            elif self.m_puzzle_type == PuzzleType.DOOR:
                image_path = os.path.join(base_path, '..', 'resources', 'graphics', 'door.png')
            elif self.m_puzzle_type == PuzzleType.PRESSURE_PLATE:
                image_path = os.path.join(base_path, '..', 'resources', 'graphics', 'pressure_plate.png')
            
            self.m_image = pg.image.load(image_path).convert_alpha()
            self.m_image = pg.transform.scale(self.m_image, (int(self._size.x), int(self._size.y)))
            
        except:

            self.m_image = pg.Surface((int(self._size.x), int(self._size.y)), pg.SRCALPHA)
            if self.m_puzzle_type == PuzzleType.MOVABLE_BLOCK:
                self.m_image.fill((139, 69, 19))
            elif self.m_puzzle_type == PuzzleType.SWITCH:
                color = (0, 255, 0) if self.m_is_activated else (255, 0, 0)
                self.m_image.fill(color)
            elif self.m_puzzle_type == PuzzleType.DOOR:
                color = (100, 100, 100) if not self.m_is_activated else (200, 200, 200)
                #self.m_image.fill(color)
            elif self.m_puzzle_type == PuzzleType.PRESSURE_PLATE:
                color = (255, 255, 0) if self.m_is_activated else (150, 150, 0)
                self.m_image.fill(color)

    def render(self, surface):
        if self.m_image:
            pos = self.get_position()
            surface.blit(self.m_image, (int(pos.x), int(pos.y)))
            
            # Debug: mostrar se está ativado
            if self.m_is_activated and self.m_puzzle_type != PuzzleType.MOVABLE_BLOCK:
                pg.draw.circle(surface, (0, 255, 0), 
                             (int(pos.x + self._size.x/2), int(pos.y + self._size.y/2)), 5)

    def update(self, delta_time):
        velocity = self.get_velocity()
        position = self._position

        if self.m_can_be_pushed:
            # Aplicar gravidade apenas para blocos móveis
            velocity.y += gravity * delta_time
            
            # Aplicar resistência ao movimento horizontal
            if not self.m_is_being_pushed:
                velocity.x *= self.m_push_resistance
                
        position += velocity * delta_time
        self.set_velocity(velocity)
        self.set_position(position)
        
        # Reset do estado de empurrar
        self.m_is_being_pushed = False

    def activate(self):
        """Ativa o puzzle (interruptor, placa de pressão, etc.)"""
        if not self.m_is_activated:
            self.m_is_activated = True
            self._load_image()  # Recarregar imagem com novo estado
            return True
        return False

    def deactivate(self):
        """Desativa o puzzle"""
        if self.m_is_activated:
            self.m_is_activated = False
            self._load_image()  # Recarregar imagem com novo estado
            return True
        return False

    def can_be_pushed(self):
        return self.m_can_be_pushed

    def push(self, push_velocity):
        """Empurra o objeto (apenas blocos móveis)"""
        if self.m_can_be_pushed:
            current_velocity = self.get_velocity()
            self.set_velocity(pg.math.Vector2(push_velocity.x, current_velocity.y))
            self.m_is_being_pushed = True

    def get_puzzle_type(self):
        return self.m_puzzle_type

    def is_activated(self):
        return self.m_is_activated

    def is_solid(self):
        """Retorna se o objeto é sólido (bloqueia movimento)"""
        if self.m_puzzle_type == PuzzleType.DOOR:
            return not self.m_is_activated  # Porta aberta não é sólida
        return True  # Outros puzzles são sólidos