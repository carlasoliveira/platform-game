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
        dynamic_object.m_is_on_ground = False
        
        for platform in platforms:
            colliding, ds = self.check_collider(platform, dynamic_object)
            abs_ds_x = abs(ds.x)
            abs_ds_y = abs(ds.y)

            if colliding:
                dyn_pos = dynamic_object.get_position()

                if abs_ds_y <= abs_ds_x:
                    dyn_pos.y += ds.y
                    dynamic_object.set_velocity(pg.math.Vector2(dynamic_object.get_velocity().x, 0))

                    if ds.y < 0:
                        dynamic_object.m_is_on_ground = True  

                elif abs_ds_x < abs_ds_y:
                    dyn_pos.x += ds.x
                    dynamic_object.set_velocity(pg.math.Vector2(0, dynamic_object.get_velocity().y))

                dynamic_object.set_position(dyn_pos)

    def check_collectible_collision(self, player, collectibles):
        for collectible in collectibles:
            if not collectible.is_collected():
                colliding, _ = self.check_collider(collectible, player)
                if colliding and collectible.get_type() == "key":
                    points = collectible.collect()
                    player.collect_points(points)
                elif colliding and player.can_collect(collectible):
                    points = collectible.collect()
                    player.collect_points(points)
                    print(f"Pastor {player.get_player_type()} coletou {collectible.get_type()}! +{points} pontos")

    def check_puzzle_collision(self, player, puzzles):
        """Verifica colisões entre player e puzzles"""
        for puzzle in puzzles:
            colliding, ds = self.check_collider(puzzle, player)
            abs_ds_x = abs(ds.x)
            abs_ds_y = abs(ds.y)

            if colliding:
                # Diferentes comportamentos para diferentes tipos de puzzle
                if puzzle.get_puzzle_type() == "movable_block":
                    self._handle_movable_block_collision(player, puzzle, ds, abs_ds_x, abs_ds_y)
                elif puzzle.get_puzzle_type() == "switch":
                    self._handle_switch_collision(player, puzzle, ds, abs_ds_x, abs_ds_y)
                elif puzzle.get_puzzle_type() == "door":
                    self._handle_door_collision(player, puzzle, ds, abs_ds_x, abs_ds_y)
                elif puzzle.get_puzzle_type() == "pressure_plate":
                    self._handle_pressure_plate_collision(player, puzzle)

    def _handle_movable_block_collision(self, player, block, ds, abs_ds_x, abs_ds_y):
        """Trata colisão com bloco móvel - jogador pode empurrar"""
        player_pos = player.get_position()
        player_velocity = player.get_velocity()
        
        if abs_ds_y <= abs_ds_x:  # Colisão vertical
            player_pos.y += ds.y
            player.set_velocity(pg.math.Vector2(player_velocity.x, 0))
            
            if ds.y < 0:
                player.m_is_on_ground = True
                
        elif abs_ds_x < abs_ds_y:  
            if ds.x > 0:
                push_direction = -1
            else:
                push_direction = 1
            
            push_force = 30.0

            push_velocity = pg.math.Vector2(push_direction * push_force, 0)
            block.push(push_velocity)
            
            # Pequeno empurrão para o jogador também
            player_pos.x += ds.x * 0.1
            
        player.set_position(player_pos)

    def _handle_switch_collision(self, player, switch, ds, abs_ds_x, abs_ds_y):
        """Trata colisão com interruptor - ativar/desativar"""
        # Jogador não atravessa o interruptor
        player_pos = player.get_position()
        
        if abs_ds_y <= abs_ds_x:
            player_pos.y += ds.y
            player.set_velocity(pg.math.Vector2(player.get_velocity().x, 0))
            if ds.y < 0:
                player.m_is_on_ground = True
        else:
            player_pos.x += ds.x
            player.set_velocity(pg.math.Vector2(0, player.get_velocity().y))
        
        player.set_position(player_pos)
        
        # Ativar interruptor se jogador está em cima
        if ds.y < 0 and abs_ds_y <= abs_ds_x:
            if switch.activate():
                print(f"Interruptor ativado por {player.get_player_type()}!")

    def _handle_door_collision(self, player, door, ds, abs_ds_x, abs_ds_y):
        """Trata colisão com porta - bloqueia se fechada"""
        print(f"Passou na Porta!")

        # Se porta está aberta (ativada), jogador passa através

    def _handle_pressure_plate_collision(self, player, plate):
        """Trata colisão com placa de pressão - ativa enquanto jogador está em cima"""
        if plate.activate():
            print(f"Placa de pressão ativada por {player.get_player_type()}!")

    def resolve_puzzle_physics(self, puzzles, platforms):
        """Resolve física dos puzzles (colisão com plataformas)"""
        for puzzle in puzzles:
            if puzzle.can_be_pushed():  # Apenas blocos móveis têm física
                self.resolve_collision(puzzle, platforms)
