import os
import pygame

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
            "1...c..............1",
            "11111..c...........1",
            "1......11111111....1",
            "1.........c........1",
            "1.............11...1",
            "11111..c...........1",
            "1..................1",
            "1......1111111111111",
            "1..111.....c.......1",
            "1........c.........1",
            "11111111111111111111"
        ]

        self.background = self._load_background()
        self.platforms = self._load_tiles()
        self.collectibles = self._load_collectibles()
        self.player_sprites = self.load_player_sprites()
        self.player = Player(
            position=pygame.math.Vector2(100, 600),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(15, 15),
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]
        )
        
    def resolve_collisions(self):
        from collider import Collider
        collider = Collider()
        collider.resolve_collision(self.player, self.platforms)
        collider.check_collectible_collision(self.player, self.collectibles)


    def update(self, delta_time):
        self.player.update(delta_time)
        # for platform in self.platforms:
        # platform.update(delta_time, self.map)
    
    def keyboard_events(self):
        self.player.verify_keyboard()
        
    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_collectibles()
        self.draw_score()
        self.player.render(self.screen)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)

    def draw_collectibles(self):
        for collectible in self.collectibles:
            collectible.render(self.screen)

    def draw_score(self):
        score_text = self.font.render(f"Pontos: {self.player.get_score()}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

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
        """Carrega coletáveis do mapa baseado na posição dos 'c'"""
        collectibles = []
        tile_size = 64
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "c":
                    position = pygame.math.Vector2(x * tile_size + 20, y * tile_size + 20)
                    size = pygame.math.Vector2(24, 24)  # Coletáveis menores que tiles
                    collectible = Collectible(position, size, points=10)
                    collectibles.append(collectible)
        return collectibles

    def load_player_sprites(self):
        base_path = os.path.dirname(__file__)
        idle_path = os.path.join(base_path, '..', 'resources', 'idle', '1.JPEG')
        idle = [pygame.transform.scale(pygame.image.load(idle_path), (128, 80))]
        right = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, '..', 'resources', 'run', f'{i}.JPEG')
                ), (15, 15)
            )
            for i in range(1,4)
        ]
        left = [pygame.transform.flip(img, True, False) for img in right]
        idle_left = [pygame.transform.flip(img, True, False) for img in idle]
        return [idle, idle_left, right, left]
