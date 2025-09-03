from object import ObjectDynamic
from collider import Collider
from constants import gravity

import pygame as pg
from object import ObjectDynamic  
from enum import Enum
import os

class Button(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2

class Player(ObjectDynamic):
    def __init__(self, position, sprites, velocity, size, my_keys, player_type="player1"):
        super().__init__(position, size, velocity)
        self.sprites = sprites
        self.m_score = 0
        self.m_lives = 3
        self.current_animation = 'idle'
        self.last_animation = 'idle'
        self.m_move_to_right = False
        self.m_move_to_left = False
        self.m_is_on_ground = False
        self.m_my_keys = my_keys  
        self.m_player_type = player_type
        

        from collectible import CollectibleType
        if player_type == "player1":
            self.m_collectible_type = CollectibleType.WHITE_SHEEP
        else:
            self.m_collectible_type = CollectibleType.BLACK_SHEEP

        self.m_jump_sound = None
        self.m_collect_sound = None
        self.m_walk_sound = None
        
        pg.mixer.init()
        self._load_sounds()
    
    

    def render(self, surface):

        current_anim = self.sprites.get(self.current_animation)
        if current_anim:
            current_anim.update()      
            sprite = current_anim.get_current_frame()
            if sprite:
                sprite_pos = pg.math.Vector2(
                    self._position.x - (sprite.get_width() - self._size.x) // 2,
                    self._position.y - (sprite.get_height() - self._size.y)
                )
                
                surface.blit(sprite, sprite_pos)

    def update(self, delta_time):
        velocity = self.get_velocity()
        position = self._position

        velocity.y += gravity * delta_time
        position += velocity * delta_time

        self.set_velocity(velocity)
        self.set_position(position)

    def collect_points(self, points):
        self.m_score += points
        
        if points == 0:
            self.m_key_sound.play()
        elif self.m_collect_sound:
            self.m_collect_sound.play()
    
    def get_score(self):
        return self.m_score
    
    def can_collect(self, collectible):
        return collectible.get_type() == self.m_collectible_type
    
    def get_player_type(self):
        return self.m_player_type
    
    def verify_keyboard(self):
        teclas = pg.key.get_pressed()
        current_velocity = self.get_velocity()

        if teclas[self.m_my_keys[Button.LEFT.value]]:
                self.m_move_to_left = True
                print("LEFT pressed")
                self.current_animation = 'run_left'
                self.set_velocity(pg.math.Vector2(-80.0, current_velocity.y))
        elif teclas[self.m_my_keys[Button.RIGHT.value]]:
                self.m_move_to_right = True
                print("RIGHT pressed")
                self.current_animation = 'run_right'
                self.set_velocity(pg.math.Vector2(80.0, current_velocity.y))
        else:
                self.m_move_to_left = False
                self.m_move_to_right = False
                self.current_animation = 'idle'
                self.set_velocity(pg.math.Vector2(0.0, current_velocity.y))

        if teclas[self.m_my_keys[Button.UP.value]]:
            if self.m_is_on_ground:
                self.set_velocity(pg.math.Vector2(current_velocity.x, -250.0))
                print("Jumping UP")
                
                if self.m_jump_sound:
                    self.m_jump_sound.play()
        print('Is on ground:', self.m_is_on_ground)
    
    def _load_sounds(self):
        base_path = os.path.dirname(__file__)
        sounds_path = os.path.join(base_path, '..', 'resources', 'sounds')
        
        sounds_to_load = [
            ('jump.wav', 0.5, 'm_jump_sound'),
            ('collect.wav', 0.7, 'm_collect_sound'),
            ('key.wav', 0.7, 'm_key_sound'),
        ]
        #  ('walk.wav', 0.3, 'm_walk_sound') Posso adicionar depois o som de caminhando
        for filename, volume, attribute in sounds_to_load:
                sound_path = os.path.join(sounds_path, filename)
                sound = pg.mixer.Sound(sound_path)
                sound.set_volume(volume)
                setattr(self, attribute, sound)