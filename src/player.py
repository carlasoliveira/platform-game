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
        self.collider_offset = [52, 46]

    def update(self, delta_time, game_map):
        print("Atualizando jogador: posição Y =", self._position[1])
        self._velocity[1] += self.gravity
        self._position[1] += self._velocity[1]  * delta_time
        if Collider.check_collision(self._position, self._size, game_map, offset=self.collider_offset):
            self._position[1] -= self._velocity[1] * delta_time
            self._velocity[1] = 0

    def move(self, keys, game_map):
        moved = False

        if keys[pg.K_a]:
            self._position[0] -= 5   
            self.animation = 3
            moved = True
        if keys[pg.K_d]:
            self._position[0] += 5
            self.animation = 2
            moved = True
        if keys[pg.K_w]:
            self.jump()

        if not moved:
            self.animation = 0 if self.animation == 2 else 1

    def jump(self):
        self._velocity[1] = self.jump_force

    def render(self, surface):
        anims = self.sprites[self.animation]
        index = self.animation_frame // 7 % len(anims)
        surface.blit(anims[index], self._position)
        offset = (40, 8)
        collider_rect = pg.Rect(
            self._position[0] + offset[0],
            self._position[1] + offset[1],
            self._size[0],
            self._size[1]
        )
        pg.draw.rect(surface, (255, 0, 0), collider_rect, 2)
        self.animation_frame = (self.animation_frame + 1) % (len(anims) * 7)
