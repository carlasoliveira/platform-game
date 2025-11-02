import pygame as pg
from object import ObjectDynamic
from constants import gravity
import os

class PuzzleType:
    MOVABLE_BLOCK = "movable_block"
    SWITCH = "switch" 
    DOOR = "door"
    PRESSURE_PLATE = "pressure_plate"

class PressurePlate(ObjectDynamic):
    """
    Placa de pressão que pode ser ativada por objetos ou players
    """
    
    def __init__(self, position, size, plate_id, sprite_inactive, sprite_active):
        """
        Args:
            position: Posição da placa
            size: Tamanho da placa
            plate_id (str): ID único da placa de pressão
            sprite_inactive: Sprite quando não ativada
            sprite_active: Sprite quando ativada
        """
        super().__init__(position, size, pg.math.Vector2(0, 0))
        
        self.plate_id = plate_id
        self.is_activated = False
        self.sprite_inactive = sprite_inactive
        self.sprite_active = sprite_active
        
        # Histórico de ativação (para detectar mudanças)
        self.was_activated = False
        
        # Lista de objetos que estão pressionando a placa
        self.pressing_objects = set()
        
        # Preparar sprites
        self._prepare_sprites()
    
    def _prepare_sprites(self):
        """Prepara os sprites no tamanho correto"""
        if self.sprite_inactive:
            self.sprite_inactive = pg.transform.scale(
                self.sprite_inactive, (int(self._size.x), int(self._size.y)))
        
        if self.sprite_active:
            self.sprite_active = pg.transform.scale(
                self.sprite_active, (int(self._size.x), int(self._size.y)))
    
    def check_activation(self, objects_list):
        """
        Verifica se algum objeto está pressionando a placa
        
        Args:
            objects_list: Lista de objetos para verificar (players, blocos, etc.)
        """
        self.pressing_objects.clear()
        
        for obj in objects_list:
            if self._is_object_pressing(obj):
                self.pressing_objects.add(id(obj))  # Usar ID do objeto
        
        # Atualizar estado de ativação
        self.was_activated = self.is_activated
        self.is_activated = len(self.pressing_objects) > 0
        
        return self.is_activated != self.was_activated  # Retorna True se mudou de estado
    
    def _is_object_pressing(self, obj):
        """
        Verifica se um objeto específico está pressionando a placa
        Considera que o objeto precisa estar "pisando" na base da placa
        """
        try:
            obj_pos = obj.get_position()
            obj_size = obj.get_size()
            
            # Criar retângulos para verificação de colisão
            obj_rect = pg.Rect(obj_pos.x, obj_pos.y, obj_size.x, obj_size.y)
            plate_rect = pg.Rect(self._position.x, self._position.y, self._size.x, self._size.y)
            
            # Verificar se há sobreposição horizontal
            if obj_rect.colliderect(plate_rect):
                # Verificar se o objeto está "pisando" na placa (parte inferior do objeto na base da placa)
                object_bottom = obj_pos.y + obj_size.y
                plate_bottom = self._position.y + self._size.y
                
                # Tolerância de alguns pixels para consideração de "pisando"
                tolerance = 8
                return abs(object_bottom - plate_bottom) <= tolerance
                
        except AttributeError:
            # Objeto não tem métodos get_position/get_size
            return False
        
        return False
    
    def get_plate_id(self):
        """Retorna o ID da placa"""
        return self.plate_id
    
    def is_active(self):
        """Retorna se a placa está ativada"""
        return self.is_activated
    
    def state_changed(self):
        """Retorna se o estado mudou desde a última verificação"""
        return self.is_activated != self.was_activated
    
    def render(self, surface):
        """Renderiza a placa com o sprite apropriado"""
        pos = self.get_position()
        
        # Escolher sprite baseado no estado
        current_sprite = self.sprite_active if self.is_activated else self.sprite_inactive
        
        if current_sprite:
            surface.blit(current_sprite, (int(pos.x), int(pos.y)))
        
        # Debug: mostrar ID da placa e estado
        if hasattr(self, '_debug_font'):
            text = self._debug_font.render(f"{self.plate_id}: {'ON' if self.is_activated else 'OFF'}", 
                                         True, (255, 255, 255))
            surface.blit(text, (int(pos.x), int(pos.y - 20)))
    
    def update(self, delta_time):
        """Atualização da placa (não faz nada por enquanto)"""
        pass
    
    def get_info(self):
        """Retorna informações de debug da placa"""
        return {
            'plate_id': self.plate_id,
            'position': (self._position.x, self._position.y),
            'size': (self._size.x, self._size.y),
            'is_activated': self.is_activated,
            'pressing_objects_count': len(self.pressing_objects)
        }

class Puzze(ObjectDynamic):
    def __init__(self, position, size, velocity, puzzle_type=PuzzleType.MOVABLE_BLOCK, custom_image=None):
        super().__init__(position, size, velocity)
        self.m_puzzle_type = puzzle_type
        self.m_is_activated = False
        self.m_can_be_pushed = puzzle_type == PuzzleType.MOVABLE_BLOCK
        self.m_is_being_pushed = False
        self.m_push_resistance = 0.8
        self.m_image = None
        self.m_custom_image = custom_image
        self._load_image()

    def _load_image(self):
        # Se uma imagem customizada foi fornecida, use-a
        if self.m_custom_image is not None:
            self.m_image = self.m_custom_image
            return
            
        try:
            base_path = os.path.dirname(__file__)
            

            if self.m_puzzle_type == PuzzleType.MOVABLE_BLOCK:
                image_path = os.path.join(base_path, '..', 'resources', 'graphics', 'obstaculo.png')
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