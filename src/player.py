from object import ObjectDynamic
from collider import Collider

import pygame as pg
from object import ObjectDynamic  
from enum import Enum

class Button(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2

class Player(ObjectDynamic):
    def __init__(self, position, sprites, velocity, size, my_keys):
        super().__init__(position, size, velocity)
        self.sprites = sprites
        self.m_score = 0
        self.m_lives = 3
        self.animation = 0
        self.animation_frame = 0
        self.last_animation = 0
        self.m_move_to_right = False
        self.m_move_to_left = False
        self.m_is_on_ground = False
        self.m_my_keys = my_keys  
        self.gravity = 50.8
    
    

    def render(self, surface):
        anims = self.sprites[self.animation]
        index = self.animation_frame // 7 % len(anims)
        surface.blit(anims[index], self._position)
        self.animation_frame = (self.animation_frame + 1) % (len(anims) * 7)

    def update(self, delta_time):
        velocity = self.get_velocity()
        position = self._position

        velocity.y += self.gravity * delta_time
        position += velocity * delta_time

        self.set_velocity(velocity)
        self.set_position(position)

    def verify_keyboard(self):
        teclas = pg.key.get_pressed()
        current_velocity = self.get_velocity()

        if teclas[self.m_my_keys[Button.LEFT.value]]:
                self.m_move_to_left = True
                print("LEFT pressed")
                self.animation = 3
                self.set_velocity(pg.math.Vector2(-30.0, current_velocity.y))
        elif teclas[self.m_my_keys[Button.RIGHT.value]]:
                self.m_move_to_right = True
                print("RIGHT pressed")
                self.animation = 2
                self.set_velocity(pg.math.Vector2(30.0, current_velocity.y))
        else:
                # Para o movimento horizontal quando nenhuma tecla de direção está pressionada
                self.m_move_to_left = False
                self.m_move_to_right = False
                self.animation = 2  # Volta para animação idle
                self.set_velocity(pg.math.Vector2(0.0, current_velocity.y))

        if teclas[self.m_my_keys[Button.UP.value]]:
            if self.m_is_on_ground:
                self.set_velocity(pg.math.Vector2(current_velocity.x, -100.0))
                print("Jumping UP")
        print('Is on ground:', self.m_is_on_ground)