import os
import pygame

from animated_gif import AnimatedGif
from Platform import Platform
from player import Player
from collectible import Collectible
class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Font para o score
        self.map = [
            "11111111111111111111",
            "1...b..............1",
            "11111..w...........1",
            "1......11111111....1",
            "1.........b........1",
            "1.............11...1",
            "11111..w...........1",
            "1..................1",
            "1......1111111111111",
            "1..111.....b.......1",
            "1........w.........1",
            "11111111111111111111"
        ]

        self.background = self._load_background()
        self.platforms = self._load_tiles()
        self.collectibles = self._load_collectibles()
        self.player_sprites = self.load_player_sprites()
        
        # Player 1 (setas) - coleta ovelhas brancas
        self.player1 = Player(
            position=pygame.math.Vector2(100, 600),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),  # Hitbox menor que o sprite
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
            player_type="player1"
        )
        
        # Player 2 (A,W,D) - coleta ovelhas pretas
        self.player2 = Player(
            position=pygame.math.Vector2(200, 600),
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
        # Score Player 1 (ovelhas brancas)
        score1_text = self.font.render(f"Player 1 (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        self.screen.blit(score1_text, (10, 10))
        
        # Score Player 2 (ovelhas pretas)
        score2_text = self.font.render(f"Player 2 (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        self.screen.blit(score2_text, (10, 50))

    def _load_background(self):
        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, '..', 'resources', 'graphics', 'background.png')
        bg = pygame.image.load(bg_path)
        return pygame.transform.scale(bg, (1280, 768))

    def _load_tiles(self):
        tiles = []
        tile_size = 64
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "1":
                    position = pygame.math.Vector2(x * tile_size, y * tile_size)
                    size = pygame.math.Vector2(tile_size, tile_size)
                    tile = Platform(position, size)
                    tiles.append(tile)
        return tiles

    def _load_collectibles(self):
        from collectible import CollectibleType
        collectibles = []
        tile_size = 64
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "w":
                    position = pygame.math.Vector2(x * tile_size + 20, y * tile_size + 20)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(position, size, CollectibleType.WHITE_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "b":
                    position = pygame.math.Vector2(x * tile_size + 20, y * tile_size + 20)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(position, size, CollectibleType.BLACK_SHEEP, points=10)
                    collectibles.append(collectible)
        return collectibles

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
