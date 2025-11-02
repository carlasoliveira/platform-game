import pygame
from object import ObjectStatic
from constants import TILE_SIZE

class ControlledBlockType:

    DISAPPEAR_WHEN_ACTIVE = "disappear_when_active"
    APPEAR_WHEN_ACTIVE = "appear_when_active"

class ControlledBlock(ObjectStatic):

    
    def __init__(self, position, size, pressure_plate_id, block_type, sprite_normal, sprite_disabled=None):

        super().__init__(position, size)
        
        self.pressure_plate_id = pressure_plate_id
        self.block_type = block_type
        self.sprite_normal = sprite_normal
        self.sprite_disabled = sprite_disabled
        
        # Estado do bloco
        self.is_pressure_plate_active = False
        self.is_solid = True
        self.is_visible = True
        
        # Preparar sprites
        self._prepare_sprites()
        self._update_state()
    
    def _prepare_sprites(self):
        """Prepara os sprites em diferentes tamanhos"""
        if self.sprite_normal:
            self.sprite_normal = pygame.transform.scale(
                self.sprite_normal, (int(self._size.x), int(self._size.y)))
        
        # Não criar sprite desabilitado - usar sempre o normal
    
    def set_pressure_plate_state(self, is_active):

        if self.is_pressure_plate_active != is_active:
            self.is_pressure_plate_active = is_active
            self._update_state()
    
    def _update_state(self):
        
        if self.block_type == ControlledBlockType.DISAPPEAR_WHEN_ACTIVE:
            # Bloco sumem quando placa é ativada
            self.is_solid = not self.is_pressure_plate_active
            self.is_visible = not self.is_pressure_plate_active
            
        elif self.block_type == ControlledBlockType.APPEAR_WHEN_ACTIVE:
            # Bloco aparecem quando placa é ativada
            self.is_solid = self.is_pressure_plate_active
            self.is_visible = self.is_pressure_plate_active
    
    def render(self, surface):
        
        if not self.is_visible:
            return
        
        pos = self.get_position()
        
        # Sempre usar o sprite normal, sem efeitos
        current_sprite = self.sprite_normal
        
        if current_sprite:
            surface.blit(current_sprite, (int(pos.x), int(pos.y)))
    
    def get_pressure_plate_id(self):
        """Retorna o ID da placa de pressão associada"""
        return self.pressure_plate_id
    
    def get_block_type(self):
        """Retorna o tipo de comportamento do bloco"""
        return self.block_type
    
    def is_solid_collision(self):
        """Retorna se o bloco deve ter colisão"""
        return self.is_solid
    
    def is_visible_render(self):
        """Retorna se o bloco deve ser renderizado"""
        return self.is_visible
    
    def get_info(self):
        """Retorna informações de debug do bloco"""
        return {
            'position': (self._position.x, self._position.y),
            'size': (self._size.x, self._size.y),
            'pressure_plate_id': self.pressure_plate_id,
            'block_type': self.block_type,
            'is_pressure_plate_active': self.is_pressure_plate_active,
            'is_solid': self.is_solid,
            'is_visible': self.is_visible
        }