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
        self.m_my_keys = my_keys  
        self.gravity = 9.8  

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

    def verify_keyboard(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.m_my_keys[Button.LEFT.value]:
                self.m_move_to_left = True
                print("LEFT pressed")
                self.animation = 3 
                self.set_velocity(pg.math.Vector2(-100.0, 0.0))

            elif event.key == self.m_my_keys[Button.RIGHT.value]:
                self.m_move_to_right = True
                print("RIGHT pressed")
                self.animation = 2
                self.set_velocity(pg.math.Vector2(100.0, 0.0))

            elif event.key == self.m_my_keys[Button.UP.value]:
                print("Up pressed")
                if self.m_move_to_left:
                    self.set_velocity(pg.math.Vector2(-30.0, -2000.0))
                    print("Up to the LEFT")
                elif self.m_move_to_right:
                    self.set_velocity(pg.math.Vector2(30.0, -40.0))
                    print("Up to the RIGHT")
                else:
                    self.set_velocity(pg.math.Vector2(0.0, -350.0))
                    print("Jumping UP")

        elif event.type == pg.KEYUP:
            if event.key in [self.m_my_keys[Button.LEFT.value],
                             self.m_my_keys[Button.RIGHT.value],
                             self.m_my_keys[Button.UP.value]]:
                self.m_move_to_left = False
                self.m_move_to_right = False
                print("Key released")
                self.set_velocity(pg.math.Vector2(0.0, 0.0))
