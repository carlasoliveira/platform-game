import os
import pygame

from animated_gif import AnimatedGif
from collider import Collider
from collectible import Collectible
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SPEED, JUMP_SPEED
from Decoration import Decoration
from lava import Lava
from Platform import Platform
from player import Player
from puzze import Puzze, PuzzleType


class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.map = [
            "2......................................1",
            "2......................................1",
            "2........#.............................1",
            "2......................................1",
            "2.........@.........!..................1",
            "2...........HI.........................1",
            "2...........FG.....................K...1",
            "2...........DE..w........f.............1",
            "2.....W3333333333333333333335..........1",
            "65.....XYYYY000000000000000065.........1",
            "02..........XYYYYYYYYYYYYY00063333333337",
            "02........................XY000000YYYY00",
            "065.........................1000YZ....X0",
            "002..........B...............XYZ.......1",
            "0065.................................w.1",
            "000635....W333333U.................W3330",
            "00YYYZ....XYYYYYZ...................XYY0",
            "0Z..................43335..4335........1",
            "2...................XYYYZ..XYYYU.......1",
            "2......................................1",
            "2.s....................................1",
            "635.............f.................433337",
            "002............43333335..bse.43333700000",
            "0065888888884337000000633333370000000000",
        ]

        self.background = self._load_background()
        self.tileset = self._load_tileset()
        self.platforms = self._load_platforms()
        self.decorations = self._load_decorations()
        self.doors = self._load_doors()  # Portas separadas para controle especial
        self.collectibles = self._load_collectibles()
        self.puzzles = self._load_puzzles()
        self.lavas = self._load_lava()
        self.player_sprites = self.load_player_sprites()
        self.player_sprites2 = self.load_player_sprites2()
        self._load_background_music()
        self.collider = Collider()
        self.game_over = False
        self.has_key = False  # Variável para registrar se a chave foi coletada
        
        # Variáveis para controle da porta
        self.door_opening = False  # Flag para indicar se a porta está sendo aberta
        self.door_open_timer = 0.0  # Timer para delay de abertura da porta
        self.door_open_delay = 0.3  # Delay de 0.3s para abrir a porta
        
        # Variáveis para detecção de vitória
        self.both_players_at_door_timer = 0.0  # Timer para ambos jogadores na porta
        self.victory_timer_threshold = 1.5  # 1.5 segundos para vitória
        self.victory_achieved = False  # Flag de vitória
        
        # Carrega sons
        self._load_door_sound()

        self.player1 = Player(
            position=pygame.math.Vector2(568, 620),
            sprites=self.player_sprites2,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
            player_type="player1"
        )

        self.player2 = Player(
            position=pygame.math.Vector2(650, 620),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),
            my_keys=[pygame.K_a, pygame.K_d, pygame.K_w],
            player_type="player2"
        )
        base_path = os.path.dirname(__file__)
        font_path = os.path.join(
            base_path, '..', 'resources', 'font', 'PotatoFont.ttf')
        self.font = pygame.font.Font(font_path, 36)
        self.title_font = pygame.font.Font(font_path, 74)
        self.subtitle_font = pygame.font.Font(font_path, 36)
        self.instruction_font = pygame.font.Font(font_path, 28)

    def resolve_collisions(self):

        self.collider.resolve_collision(self.player1, self.platforms)
        self.collider.resolve_collision(self.player2, self.platforms)

        key_collected1 = self.collider.check_collectible_collision(
            self.player1, self.collectibles)
        key_collected2 = self.collider.check_collectible_collision(
            self.player2, self.collectibles)
        
        # Atualiza o estado da chave se algum jogador coletou
        if key_collected1 or key_collected2:
            self.has_key = True

        self.collider.check_puzzle_collision(self.player1, self.puzzles)
        self.collider.check_puzzle_collision(self.player2, self.puzzles)

        # Verifica colisão com portas e abre se tiver chave
        self._check_door_interactions()

        game_over1 = self.collider.resolve_lava_collision(
            self.player1, self.lavas)
        game_over2 = self.collider.resolve_lava_collision(
            self.player2, self.lavas)
        self.game_over = game_over1 or game_over2

        self.collider.resolve_puzzle_physics(self.puzzles, self.platforms)

    def _check_door_interactions(self):
        """Verifica se algum jogador tocou na porta e abre se tiver a chave"""
        if self.has_key and not self.door_opening:
            # Verifica se alguma porta foi tocada
            door_touched = False
            for door in self.doors:
                # Verifica colisão do player1 com qualquer parte da porta
                colliding1, _ = self.collider.check_collider(door, self.player1)
                # Verifica colisão do player2 com qualquer parte da porta
                colliding2, _ = self.collider.check_collider(door, self.player2)
                
                if (colliding1 or colliding2) and not door.get_is_open():
                    door_touched = True
                    break
            
            # Se alguma parte da porta foi tocada, inicia o processo de abertura
            if door_touched:
                # Toca o som
                if self.door_sound:
                    self.door_sound.play()
                
                # Inicia o timer de abertura
                self.door_opening = True
                self.door_open_timer = 0.0
                print("Porta sendo aberta com a chave...")

    def _check_victory_condition(self, delta_time):
        """Verifica se ambos jogadores estão na porta aberta por 1.5s"""
        # Primeiro verifica se pelo menos uma porta está aberta
        any_door_open = any(door.get_is_open() for door in self.doors)
        
        if not any_door_open:
            self.both_players_at_door_timer = 0.0
            return
        
        # Verifica se ambos jogadores estão tocando em qualquer porta aberta
        player1_at_door = False
        player2_at_door = False
        
        for door in self.doors:
            if door.get_is_open():
                colliding1, _ = self.collider.check_collider(door, self.player1)
                colliding2, _ = self.collider.check_collider(door, self.player2)
                
                if colliding1:
                    player1_at_door = True
                if colliding2:
                    player2_at_door = True
        
        # Verifica se ambos jogadores estão no chão (não pulando)
        player1_on_ground = self.player1.m_is_on_ground
        player2_on_ground = self.player2.m_is_on_ground
        
        # Se ambos estão na porta e no chão, incrementa o timer
        if player1_at_door and player2_at_door and player1_on_ground and player2_on_ground:
            self.both_players_at_door_timer += delta_time
            
            if self.both_players_at_door_timer >= self.victory_timer_threshold:
                self.victory_achieved = True
                print("Vitoria! !")
        else:
            # Reset o timer se a condição não for atendida
            self.both_players_at_door_timer = 0.0

    def reset_game_state(self):
        """Reseta o estado do jogo, incluindo chave e portas"""
        self.has_key = False
        self.door_opening = False
        self.door_open_timer = 0.0
        self.both_players_at_door_timer = 0.0
        self.victory_achieved = False
        
        # Fecha todas as portas
        for door in self.doors:
            door.close_door()

    def update(self, delta_time):
        self.player1.update(delta_time)
        self.player2.update(delta_time)

        for puzzle in self.puzzles:
            puzzle.update(delta_time)
        
        # Atualiza timer de abertura da porta
        if self.door_opening:
            self.door_open_timer += delta_time
            if self.door_open_timer >= self.door_open_delay:
                # Abre todas as portas após o delay
                for door in self.doors:
                    if not door.get_is_open():
                        door.open_door()
                self.door_opening = False
                self.door_open_timer = 0.0
        
        # Verifica se ambos jogadores estão na porta (quando ela estiver aberta)
        if self.has_key and not self.victory_achieved:
            self._check_victory_condition(delta_time)

    def keyboard_events(self):
        self.player1.verify_keyboard()
        self.player2.verify_keyboard()

    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_score()
        self.player1.render(self.screen)
        self.player2.render(self.screen)
        
        # Desenha popup de vitória se necessário
        if self.victory_achieved:
            self._draw_victory()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)
        for decoration in self.decorations:
            decoration.render(self.screen)
        for door in self.doors:
            door.render(self.screen)
        for collectible in self.collectibles:
            collectible.render(self.screen)
        for puzzle in self.puzzles:
            puzzle.render(self.screen)
        for lava in self.lavas:
            lava.render(self.screen)

    def draw_score(self):
        score1_text = self.font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        self.screen.blit(score1_text, (10, 10))

        score2_text = self.font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        self.screen.blit(score2_text, (10, 50))
        
        # Desenha indicador de chave
        if self.has_key:
            key_text = self.font.render("CHAVE COLETADA!", True, (255, 255, 0))
            self.screen.blit(key_text, (10, 90))
        
        # Desenha barra de progresso para vitória
        if self.both_players_at_door_timer > 0 and not self.victory_achieved:
            progress = min(self.both_players_at_door_timer / self.victory_timer_threshold, 1.0)
            self._draw_victory_progress(progress)

    def _draw_victory_progress(self, progress):
        """Desenha barra de progresso para vitória"""
        # Texto indicativo
        progress_text = self.instruction_font.render(
            "Ambos na porta! Aguarde...", True, (255, 255, 0))
        text_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(progress_text, text_rect)
        
        # Barra de progresso
        bar_width = 300
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 170
        
        # Fundo da barra
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (100, 100, 100), background_rect)
        
        # Progresso da barra
        progress_width = int(bar_width * progress)
        progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
        color = (255, 255 - int(progress * 255), 0)  # Amarelo para verde
        pygame.draw.rect(self.screen, color, progress_rect)
        
        # Borda da barra
        pygame.draw.rect(self.screen, (255, 255, 255), background_rect, 2)

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Texto principal "GAME OVER"
        title_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # Texto de pontuação
        score1_text = self.subtitle_font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        score1_rect = score1_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score1_text, score1_rect)

        score2_text = self.subtitle_font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        score2_rect = score2_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score2_text, score2_rect)

        # Instruções para reiniciar
        restart_text = self.instruction_font.render(
            "Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, restart_rect)

        # Instruções para sair
        quit_text = self.instruction_font.render(
            "Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(quit_text, quit_rect)

    def _draw_victory(self):
        """Desenha a tela de vitória"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 50, 0))  # Verde escuro para vitória
        self.screen.blit(overlay, (0, 0))

        # Texto principal "VITÓRIA!"
        title_text = self.title_font.render("VITÓRIA!", True, (50, 255, 50))
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # Texto de fase completada
        stage_text = self.subtitle_font.render(
            "Fase Completada!", True, (255, 255, 255))
        stage_rect = stage_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(stage_text, stage_rect)

        # Texto de pontuação final
        score1_text = self.instruction_font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        score1_rect = score1_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score1_text, score1_rect)

        score2_text = self.instruction_font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        score2_rect = score2_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(score2_text, score2_rect)

        # Instruções para continuar
        restart_text = self.instruction_font.render(
            "Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

        # Instruções para sair
        quit_text = self.instruction_font.render(
            "Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
        self.screen.blit(quit_text, quit_rect)

    def _load_background(self):
        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, '..', 'resources',
                               'graphics', 'background.png')
        bg = pygame.image.load(bg_path)
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def _load_tileset(self):
        base_path = os.path.dirname(__file__)
        tileset_path = os.path.join(
            base_path, '..', 'resources', 'graphics', 'tile1.png')
        tileset = pygame.image.load(tileset_path)
        return tileset

    def get_sprite(self, tileset, x, y, tile_size):
        sprite = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        sprite.blit(tileset, (0, 0), (x * tile_size,
                    y * tile_size, tile_size, tile_size))
        return sprite

    def _load_collectibles(self):
        from collectible import CollectibleType
        collectibles = []
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "w":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(
                        position, size, CollectibleType.WHITE_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "s":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(
                        position, size, CollectibleType.BLACK_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "K":
                    position = pygame.math.Vector2(x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(28, 28)
                    collectible = Collectible(position, size, CollectibleType.KEY, points=0)
                    collectibles.append(collectible)
        return collectibles

    def _load_lava(self):
        lavas = []
        pixel = self.get_sprite(self.tileset, 1, 46, 8)
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "8":
                    img = pygame.transform.scale(pixel, (TILE_SIZE, TILE_SIZE))
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    lava = Lava(position, size, img)
                    lavas.append(lava)
        return lavas

    def _load_puzzles(self):
        puzzles = []

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "B":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    velocity = pygame.math.Vector2(0, 0)
                    puzzle = Puzze(position, size, velocity,
                                   PuzzleType.MOVABLE_BLOCK)
                    puzzles.append(puzzle)
        return puzzles

    def _load_platforms(self):
        platforms = []

        plataform_tile_map = {
            "0": self.get_sprite(self.tileset, 1, 8, 16), # tile_DIRT
            "1": self.get_sprite(self.tileset, 0, 8, 16), # tile_DIRT_EDGE_LEFT
            "2": self.get_sprite(self.tileset, 2, 8, 16), # tile_DIRT_EDGE_RIGHT

            "3": self.get_sprite(self.tileset, 1, 7, 16), # tile_GRASS
            "4": self.get_sprite(self.tileset, 0, 7, 16), # tile_GRASS_EDGE_LEFT
            "5": self.get_sprite(self.tileset, 2, 7, 16), # tile_GRASS_EDGE_RIGHT

            "W": self.get_sprite(self.tileset, 0, 10, 16), # tile_ONLY_GRASS_LEFT
            "U": self.get_sprite(self.tileset, 2, 10, 16), # tile_ONLY_GRASS_RIGHT
            "V": self.get_sprite(self.tileset, 1, 10, 16), # tile_ONLY_GRASS_CENTER

            
            "6": self.get_sprite(self.tileset, 4, 8, 16), # tile_GRASS_EDGE_TOP_RIGHT
            "7": self.get_sprite(self.tileset, 5, 8, 16), # tile_GRASS_EDGE_TOP_LEFT

            "X": self.get_sprite(self.tileset, 0, 9, 16), # tile_DIRT_BOTTOM_LEFT
            "Y": self.get_sprite(self.tileset, 1, 9, 16), # tile_DIRT_BOTTOM
            "Z": self.get_sprite(self.tileset, 2, 9, 16), # tile_DIRT_BOTTOM_right
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in plataform_tile_map:
                    img = pygame.transform.scale(
                        plataform_tile_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    platforms.append(Platform(position, size, img))

        return platforms

    def _load_decorations(self):
        decorations = []

        decoration_tile_map = {
            "a": self.get_sprite(self.tileset, 9, 10, 16),  # tile_WEEDS_1
            "b": self.get_sprite(self.tileset, 10, 10, 16),  # tile_WEEDS_2
            "c": self.get_sprite(self.tileset, 11, 10, 16),  # tile_WEEDS_3

            "d": self.get_sprite(self.tileset, 11, 12, 16),  # tile_FLOWERS_1
            "e": self.get_sprite(self.tileset, 11, 13, 16),  # tile_FLOWERS_2

            "f": self._make_decoration_block_auto((9, 11), 3, 1),

            "@": self._make_decoration_block_auto((10, 35), 8, 4), # tile_block_WALLS
            "#": self._make_decoration_block_auto((0, 31), 10, 2), # tile_block_ROOF
            "!": self._make_decoration_block_auto((17, 23), 4, 4), # tile_block_POÇO
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in decoration_tile_map:
                    block_surface = decoration_tile_map[tile_char]

                    # Verifica se é o bloco 3x3 (ou outro maior que 1 tile)
                    if tile_char == "@":
                        img = pygame.transform.scale(block_surface, (8 * TILE_SIZE, 4 * TILE_SIZE))
                        size = pygame.math.Vector2(8 * TILE_SIZE, 4 * TILE_SIZE)
                    elif tile_char == "#":
                        img = pygame.transform.scale(block_surface, (10 * TILE_SIZE, 2 * TILE_SIZE))
                        size = pygame.math.Vector2(10 * TILE_SIZE, 2 * TILE_SIZE)
                    elif tile_char == "f":
                        img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 1 * TILE_SIZE))
                        size = pygame.math.Vector2(3 * TILE_SIZE, 1 * TILE_SIZE)
                    elif tile_char == "!":
                        img = pygame.transform.scale(block_surface, (4 * TILE_SIZE, 4 * TILE_SIZE))
                        size = pygame.math.Vector2(4 * TILE_SIZE, 4 * TILE_SIZE)
                    else:
                        img = pygame.transform.scale(block_surface, (TILE_SIZE, TILE_SIZE))
                        size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)

                    position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    decorations.append(Decoration(position, size, img))

        return decorations


    def _make_decoration_block_auto(self, start_tile, block_width, block_height, tile_size=16):
        block_surface = pygame.Surface((block_width * tile_size, block_height * tile_size), pygame.SRCALPHA)

        start_x, start_y = start_tile
        for row in range(block_height):
            for col in range(block_width):
                tx = start_x + col
                ty = start_y + row
                img = self.get_sprite(self.tileset, tx, ty, tile_size)  # usa 16 aqui
                block_surface.blit(img, (col * tile_size, row * tile_size))

        return block_surface

    def _load_doors(self):
        from door import Door
        doors = []

        # Sprites para porta fechada
        door_closed_map = {
            "D": self.get_sprite(self.tileset, 2, 45, 16), #tile_DOOR_BOT_L_CLOSED
            "E": self.get_sprite(self.tileset, 3, 45, 16), #tile_DOOR_BOT_R_CLOSED
            "F": self.get_sprite(self.tileset, 2, 44, 16), #tile_DOOR_MID_L_CLOSED
            "G": self.get_sprite(self.tileset, 3, 44, 16), #tile_DOOR_MID_R_CLOSED
            "H": self.get_sprite(self.tileset, 2, 43, 16), #tile_DOOR_TOP_L_CLOSED
            "I": self.get_sprite(self.tileset, 3, 43, 16), #tile_DOOR_TOP_R_CLOSED
        }

        # Sprites para porta aberta (usando coordenadas diferentes no tileset)
        door_open_map = {
            "D": self.get_sprite(self.tileset, 0, 45, 16), #tile_DOOR_BOT_L_OPEN
            "E": self.get_sprite(self.tileset, 1, 45, 16), #tile_DOOR_BOT_R_OPEN
            "F": self.get_sprite(self.tileset, 0, 44, 16), #tile_DOOR_MID_L_OPEN
            "G": self.get_sprite(self.tileset, 1, 44, 16), #tile_DOOR_MID_R_OPEN
            "H": self.get_sprite(self.tileset, 0, 43, 16), #tile_DOOR_TOP_L_OPEN
            "I": self.get_sprite(self.tileset, 1, 43, 16), #tile_DOOR_TOP_R_OPEN
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in door_closed_map:
                    closed_img = pygame.transform.scale(
                        door_closed_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    open_img = pygame.transform.scale(
                        door_open_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    door = Door(position, size, closed_img, open_img)
                    doors.append(door)

        return doors

    def load_player_sprites(self):

        base_path = os.path.dirname(__file__)
        sprite_size = (32, 48)
        sprite_size_die = (16, 16)

        idle_path = os.path.join(
            base_path, '..', 'resources', 'idle', 'Player_Idle.gif')
        idle_gif = AnimatedGif(idle_path, sprite_size)
        run_path = os.path.join(
            base_path, '..', 'resources', 'run', 'Player_Run.gif')
        run_gif = AnimatedGif(run_path, sprite_size)
        run_left_gif = run_gif.get_flipped_frames()

        die_path = os.path.join(
            base_path, '..', 'resources', 'die', 'Player_Die.gif')
        die_gif = AnimatedGif(die_path, sprite_size_die)

        return {
            'idle': idle_gif,
            'idle_left': idle_gif,
            'run_right': run_gif,
            'run_left': run_left_gif,
            'die': die_gif
        }

    def load_player_sprites2(self):

        base_path = os.path.dirname(__file__)
        sprite_size = (32, 48)
        sprite_size_die = (20, 20)

        idle_path = os.path.join(
            base_path, '..', 'resources', 'idle', 'Player_Idle_b.gif')
        idle_gif = AnimatedGif(idle_path, sprite_size)
        run_path = os.path.join(
            base_path, '..', 'resources', 'run', 'Player_Run_b.gif')
        run_gif = AnimatedGif(run_path, sprite_size)
        run_left_gif = run_gif.get_flipped_frames()

        die_path = os.path.join(
            base_path, '..', 'resources', 'die', 'Player_Die.gif')
        die_gif = AnimatedGif(die_path, sprite_size_die)

        return {
            'idle': idle_gif,
            'idle_left': idle_gif,
            'run_right': run_gif,
            'run_left': run_left_gif,
            'die': die_gif
        }

    def _load_door_sound(self):
        """Carrega o som para quando a porta é ativada"""
        try:
            base_path = os.path.dirname(__file__)
            sound_path = os.path.join(base_path, '..', 'resources', 'sounds', 'key.wav')
            self.door_sound = pygame.mixer.Sound(sound_path)
            self.door_sound.set_volume(0.7)
        except:
            self.door_sound = None

    def _load_background_music(self):
        base_path = os.path.dirname(__file__)
        music_path = os.path.join(
            base_path, '..', 'resources', 'sounds', 'background_sound.mp3')

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def _create_fallback_sprites(self, sprite_size):

        simple_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
        simple_surface.fill((0, 255, 0))

        fake_gif = AnimatedGif.__new__(AnimatedGif)
        fake_gif.m_frames = [simple_surface]
        fake_gif.m_frame_count = 1
        fake_gif.m_current_frame = 0
        fake_gif.m_frame_timer = 0
        fake_gif.m_animation_speed = 5

        return {
            'idle': fake_gif,
            'idle_left': fake_gif,
            'run_right': fake_gif,
            'run_left': fake_gif
        }
