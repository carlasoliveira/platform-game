import os
import pygame

from animated_gif import AnimatedGif
from collider import Collider
from collectible import Collectible
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SPEED, JUMP_SPEED
from decoration import Decoration
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
            "2......................................1",
            "2................w.....................1",
            "2...3..433333333333333333333333333333337",
            "2......................................1",
            "2...w..........B......................w1",
            "65cfgh........433335..................47",
            "633333333333333333333333333333335...3..1",
            "2......................................1",
            "2...............................3......1",
            "2....435..............................31",
            "2......................................1",
            "2......4333..........3333333333333333337",
            "2...3..................................1",
            "65.....................................1",
            "02s....................................1",
            "0635...........................s.......1",
            "000633335....435...43333333333335......1",
            "2......................................1",
            "2..................................s.937",
            "2...B..B........cebcfgh...........933700",
            "633333335122..43333333333333333333700000",
            "0000000008888800000000000000000000000000",
            "0000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000",
        ]

        self.background = self._load_background()
        self.tileset = self._load_tileset()
        self.platforms = self._load_platforms()
        self.decorations = self._load_decorations()
        self.collectibles = self._load_collectibles()
        self.puzzles = self._load_puzzles()
        self.lavas = self._load_lava()
        self.player_sprites = self.load_player_sprites()
        self.player_sprites2 = self.load_player_sprites2()
        self._load_background_music()
        self.collider = Collider()
        self.game_over = False

        self.player1 = Player(
            position=pygame.math.Vector2(100, 580),
            sprites=self.player_sprites2,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
            player_type="player1"
        )

        self.player2 = Player(
            position=pygame.math.Vector2(50, 580),
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

        self.collider.check_collectible_collision(
            self.player1, self.collectibles)
        self.collider.check_collectible_collision(
            self.player2, self.collectibles)

        self.collider.check_puzzle_collision(self.player1, self.puzzles)
        self.collider.check_puzzle_collision(self.player2, self.puzzles)

        game_over1 = self.collider.resolve_lava_collision(
            self.player1, self.lavas)
        game_over2 = self.collider.resolve_lava_collision(
            self.player2, self.lavas)
        self.game_over = game_over1 or game_over2

        self.collider.resolve_puzzle_physics(self.puzzles, self.platforms)

    def update(self, delta_time):
        self.player1.update(delta_time)
        self.player2.update(delta_time)

        for puzzle in self.puzzles:
            puzzle.update(delta_time)

    def keyboard_events(self):
        self.player1.verify_keyboard()
        self.player2.verify_keyboard()

    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_score()
        self.player1.render(self.screen)
        self.player2.render(self.screen)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)
        for decoration in self.decorations:
            decoration.render(self.screen)
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
            "0": self.get_sprite(self.tileset, 1, 8, 16),  # tile_DIRT
            # tile_DIRT_EDGE_LEFT
            "1": self.get_sprite(self.tileset, 0, 8, 16),
            # tile_DIRT_EDGE_RIGHT
            "2": self.get_sprite(self.tileset, 2, 8, 16),

            "3": self.get_sprite(self.tileset, 1, 7, 16),  # tile_GRASS
            # tile_GRASS_EDGE_LEFT
            "4": self.get_sprite(self.tileset, 0, 7, 16),
            # tile_GRASS_EDGE_RIGHT
            "5": self.get_sprite(self.tileset, 2, 7, 16),

            # tile_GRASS_EDGE_TOP_LEFT
            "6": self.get_sprite(self.tileset, 4, 8, 16),
            # tile_GRASS_EDGE_TOP_RIGHT
            "7": self.get_sprite(self.tileset, 5, 8, 16),
            # tile_GRASS_EDGE_TOP_RIGHT
            "9": self.get_sprite(self.tileset, 7, 7, 16),
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

            "f": self.get_sprite(self.tileset, 9, 11, 16),  # tile_FENCE_1
            "g": self.get_sprite(self.tileset, 10, 11, 16),  # tile_FENCE_2
            "h": self.get_sprite(self.tileset, 11, 11, 16),  # tile_FENCE_3
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in decoration_tile_map:
                    img = pygame.transform.scale(
                        decoration_tile_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    decorations.append(Decoration(position, size, img))

        return decorations

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
