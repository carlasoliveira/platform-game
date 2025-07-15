import os
import pygame

from animated_gif import AnimatedGif
from Platform import Platform
from decoration import Decoration
from player import Player
from collectible import Collectible
class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Font para o score
        self.map = [
            ".......................................1",
            ".......................................1",
            ".......................................1",
            "................w......................1",
            "5..............43335...................1",
            "65.....................................1",
            "02...................................w.1",
            "0635.w............................433337",
            "000635.................................1",
            "000002...................43335.........1",
            "000002.................................1",
            "000002.................435.............1",
            "000002.................................1",
            "000002..............43335........435...1",
            "000002......435........................1",
            "000002.................................1",
            "000002............4335.........s.......1",
            "000002....................cebcfgh......1",
            "000002.........43335.....4333333335....1",
            "000002.........10002.....1000000002....1",
            "000002.........10002.....1000000002....1",
            "000002.......aa10002.....1000000002c...1",
            "0000063333333337000633333700000000633337",
            "0000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000"
        ]

        self.background = self._load_background()
        self.tileset = self._load_tileset()  # Carregar tileset
        self.platforms = self._load_tiles()
        self.collectibles = self._load_collectibles()
        self.player_sprites = self.load_player_sprites()
        
        # Carregar música de fundo
        self._load_background_music()
        
        self.player1 = Player(
            position=pygame.math.Vector2(100, 150),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),  # Hitbox menor que o sprite
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
            player_type="player1"
        )

        self.player2 = Player(
            position=pygame.math.Vector2(30, 100),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),  # Hitbox menor que o sprite
            my_keys=[pygame.K_a, pygame.K_d, pygame.K_w],
            player_type="player2"
        )
        
    def resolve_collisions(self):
        from collider import Collider
        collider = Collider()
        
        # Colisões com plataformas para ambos os players
        collider.resolve_collision(self.player1, self.platforms)
        collider.resolve_collision(self.player2, self.platforms)
        
        # Colisões com coletáveis para ambos os players
        collider.check_collectible_collision(self.player1, self.collectibles)
        collider.check_collectible_collision(self.player2, self.collectibles)


    def update(self, delta_time):
        self.player1.update(delta_time)
        self.player2.update(delta_time)
    
    def keyboard_events(self):
        self.player1.verify_keyboard()
        self.player2.verify_keyboard()
        
    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_collectibles()
        self.draw_score()
        self.player1.render(self.screen)
        self.player2.render(self.screen)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)

    def draw_collectibles(self):
        for collectible in self.collectibles:
            collectible.render(self.screen)

    def draw_score(self):
        score1_text = self.font.render(f"Player 1 (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        self.screen.blit(score1_text, (10, 10))

        score2_text = self.font.render(f"Player 2 (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        self.screen.blit(score2_text, (10, 50))

    def _load_background(self):
        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, '..', 'resources', 'graphics', 'background.png')
        bg = pygame.image.load(bg_path)
        return pygame.transform.scale(bg, (1280, 768))

    def _load_tileset(self):
        base_path = os.path.dirname(__file__)
        tileset_path = os.path.join(base_path, '..', 'resources', 'graphics', 'tile1.png')
        tileset = pygame.image.load(tileset_path)
        return tileset


    def get_sprite(self, tileset, x, y, tile_size):
        sprite = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        sprite.blit(tileset, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
        return sprite

    def _load_collectibles(self):
        from collectible import CollectibleType
        collectibles = []
        tile_size = 32  # Mesmo tamanho usado para os tiles do mapa
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "w":
                    position = pygame.math.Vector2(x * tile_size + 4, y * tile_size + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(position, size, CollectibleType.WHITE_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "s":
                    position = pygame.math.Vector2(x * tile_size + 4, y * tile_size + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(position, size, CollectibleType.BLACK_SHEEP, points=10)
                    collectibles.append(collectible)
        return collectibles

    def _load_tiles(self):

        tiles = []
        tile_size = 32

        plataform_tile_map = {
            "0": self.get_sprite(self.tileset, 1, 8, 16), #tile_DIRT
            "1": self.get_sprite(self.tileset, 0, 8, 16), #tile_DIRT_EDGE_LEFT
            "2": self.get_sprite(self.tileset, 2, 8, 16), #tile_DIRT_EDGE_RIGHT
            
            "3": self.get_sprite(self.tileset, 1, 7, 16), #tile_GRASS
            "4": self.get_sprite(self.tileset, 0, 7, 16), #tile_GRASS_EDGE_LEFT
            "5": self.get_sprite(self.tileset, 2, 7, 16), #tile_GRASS_EDGE_RIGHT

            "6": self.get_sprite(self.tileset, 4, 8, 16), #tile_GRASS_EDGE_TOP_LEFT
            "7": self.get_sprite(self.tileset, 5, 8, 16), #tile_GRASS_EDGE_TOP_RIGHT
        }

        decoration_tile_map = {
            "a": self.get_sprite(self.tileset, 9, 10, 16), #tile_WEEDS_1
            "b": self.get_sprite(self.tileset, 10, 10, 16), #tile_WEEDS_2
            "c": self.get_sprite(self.tileset, 11, 10, 16), #tile_WEEDS_3

            "d": self.get_sprite(self.tileset, 11, 12, 16), #tile_FLOWERS_1
            "e": self.get_sprite(self.tileset, 11, 13, 16), #tile_FLOWERS_2

            "f": self.get_sprite(self.tileset, 9, 11, 16), #tile_FENCE_1
            "g": self.get_sprite(self.tileset, 10, 11, 16), #tile_FENCE_2
            "h": self.get_sprite(self.tileset, 11, 11, 16), #tile_FENCE_3
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in plataform_tile_map:

                    img = pygame.transform.scale(plataform_tile_map[tile_char], (tile_size, tile_size))
                    position = pygame.math.Vector2(x * tile_size, y * tile_size)
                    size = pygame.math.Vector2(tile_size, tile_size)

                    tiles.append(Platform(position, size, img))

                if tile_char in decoration_tile_map:

                    img = pygame.transform.scale(decoration_tile_map[tile_char], (tile_size, tile_size))
                    position = pygame.math.Vector2(x * tile_size, y * tile_size)
                    size = pygame.math.Vector2(tile_size, tile_size)

                    tiles.append(Decoration(position, size, img))
        
        return tiles


    def load_player_sprites(self):
        
        base_path = os.path.dirname(__file__)
        sprite_size = (32, 48)
        
        try:

            idle_path = os.path.join(base_path, '..', 'resources', 'idle', 'Player_Idle.gif')
            idle_gif = AnimatedGif(idle_path, sprite_size)

            run_path = os.path.join(base_path, '..', 'resources', 'run', 'Player_Run.gif')
            run_gif = AnimatedGif(run_path, sprite_size)

            run_left_gif = run_gif.get_flipped_frames()
            
            return {
                'idle': idle_gif,
                'idle_left': idle_gif,  
                'run_right': run_gif,
                'run_left': run_left_gif
            }
            
        except Exception as e:
            return self._create_fallback_sprites(sprite_size)

    def _load_background_music(self):
        try:
            base_path = os.path.dirname(__file__)
            music_path = os.path.join(base_path, '..', 'resources', 'sounds', 'background_sound.mp3')

            try:
                pygame.mixer.music.load(music_path)
            except:
                music_path_wav = os.path.join(base_path, '..', 'resources', 'sounds', 'background_sound.wav')
                pygame.mixer.music.load(music_path_wav)

            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            
        except Exception as e:
            print(f"Erro ao carregar música de fundo: {e}")
    
    
    def _create_fallback_sprites(self, sprite_size):
        
        simple_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
        simple_surface.fill((0, 255, 0))
        
        fake_gif = AnimatedGif.__new__(AnimatedGif)
        fake_gif.frames = [simple_surface]
        fake_gif.frame_count = 1
        fake_gif.current_frame = 0
        fake_gif.frame_timer = 0
        fake_gif.animation_speed = 5
        
        return {
            'idle': fake_gif,
            'idle_left': fake_gif,
            'run_right': fake_gif,
            'run_left': fake_gif
        }
