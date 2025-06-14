import pygame as pg
from object import ObjectDynamic
from collider import Collider

class Player(ObjectDynamic):
    def __init__(self, sprites, position, size, velocity):
        super().__init__(position, size, velocity)
        self.sprites = sprites
        self.animation = 0
        self.animation_frame = 0
        self.gravity = 1
        self.jump_force = -22

    def update(self, delta_time, game_map):
        self._velocity[1] += self.gravity * delta_time
        self._position[1] += self._velocity[1]  * delta_time
        if Collider.check_collision(self._position, self._size, game_map):
            self._position[1] -= self._velocity[1] 
            self._velocity[1] = 0

    def move(self, keys, game_map):
        moved = False
        if keys[pg.K_a]:
            self._position[0] -= 5
            if Collider.check_collision(self._position, self._size, game_map):
                self._position[0] += 5
            else:
                self.animation = 3
                moved = True
                
        if keys[pg.K_d]:
            self._position[0] += 5
            if Collider.check_collision(self._position, self._size, game_map):
                self._position[0] -= 5
            else:
                self.animation = 2
                moved = True

        if not moved:
            self.animation = 0 if self.animation == 2 else 1

    def jump(self):
        self._velocity[1] = self.jump_force

    def render(self, surface):
        anims = self.sprites[self.animation]
        index = self.animation_frame // 7 % len(anims)
        surface.blit(anims[index], self._position)
        self.animation_frame = (self.animation_frame + 1) % (len(anims) * 7)
