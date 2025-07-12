import pygame as pg
import math

class Collider:
    

    def check_collider(self, static_object, dynamic_object):
        collision_vector = pg.math.Vector2()

        static_pos = static_object.get_position() + (static_object.get_size() / 2.0)
        dynamic_pos = dynamic_object.get_position() + (dynamic_object.get_size() / 2.0)

        distance = pg.math.Vector2(dynamic_pos.x - static_pos.x, dynamic_pos.y - static_pos.y)
        target_distance = (static_object.get_size() + dynamic_object.get_size()) / 2.0

        # static_rect = pg.Rect(
        #     static_pos.x - static_object.get_size().x / 2,
        #     static_pos.y - static_object.get_size().y / 2,
        #     static_object.get_size().x,
        #     static_object.get_size().y
        # )

        # dynamic_rect = pg.Rect(
        #     dynamic_pos.x - dynamic_object.get_size().x / 2,
        #     dynamic_pos.y - dynamic_object.get_size().y / 2,
        #     dynamic_object.get_size().x,
        #     dynamic_object.get_size().y
        # )

        # pg.draw.rect(self.screen, (255, 255, 0), static_rect, 2)
        # pg.draw.rect(self.screen, (0, 255, 0), dynamic_rect, 2)

        collision_x = abs(distance.x) < target_distance.x
        collision_vector.x = math.copysign(target_distance.x - abs(distance.x), distance.x)

        collision_y = abs(distance.y) < target_distance.y
        collision_vector.y = math.copysign(target_distance.y - abs(distance.y), distance.y)

        return collision_x and collision_y, collision_vector


    def resolve_collision(self, dynamic_object, platforms):
        # Reset m_is_on_ground no início - será True apenas se houver colisão no chão
        dynamic_object.m_is_on_ground = False
        
        for platform in platforms:
            colliding, ds = self.check_collider(platform, dynamic_object)
            abs_ds_x = abs(ds.x)
            abs_ds_y = abs(ds.y)

            if colliding:
                dyn_pos = dynamic_object.get_position()

                if abs_ds_y <= abs_ds_x:
                    # print("COLLISION DETECTED IN Y")
                    dyn_pos.y += ds.y
                    dynamic_object.set_velocity(pg.math.Vector2(dynamic_object.get_velocity().x, 0))
                    
                    # Só marca como no chão se a colisão é por baixo (player caindo)
                    if ds.y < 0:  # Player está sendo empurrado para cima (colidiu com o chão)
                        dynamic_object.m_is_on_ground = True  

                elif abs_ds_x < abs_ds_y:
                    # print("COLLISION DETECTED IN X")
                    dyn_pos.x += ds.x
                    dynamic_object.set_velocity(pg.math.Vector2(0, dynamic_object.get_velocity().y))

                dynamic_object.set_position(dyn_pos)

    def check_collectible_collision(self, player, collectibles):
        """Verifica colisão entre player e itens coletáveis"""
        for collectible in collectibles:
            if not collectible.is_collected():
                colliding, _ = self.check_collider(collectible, player)
                if colliding:
                    points = collectible.collect()
                    player.collect_points(points)
                    print(f"Coletável pego! +{points} pontos")
