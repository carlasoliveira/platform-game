import pygame as pg
from Platform import Vector
from Object import ObjectDynamic


class Obstacle(ObjectDynamic):
    def __init__(self, position: Vector, velocity: Vector, size: Vector, texture):
        super().__init__(position, size, texture, velocity)
        print("Obstaculo criado")

    def __del__(self):
        print("LIMPAR VARIAVEIS AQUI (Obstacle destruído)")
        
    def render(self, screen):
        pos = self.get_position()
        size = self.get_size()
        center = pos + (size / 2.0)

        rect = pg.Rect(
            int(center.x - size.x / 2),
            int(center.y - size.y / 2),
            int(size.x),
            int(size.y)
        )

        pg.draw.rect(screen, (30, 30, 30), rect)

    def update(self, delta_time: float):
        velocity = self.get_velocity()
        position = self.get_position()

		#Incluir o delta_time
        position.x += velocity.x * delta_time
        position.y += velocity.y * delta_time

        self.set_velocity(velocity)
        self.set_position(position)
