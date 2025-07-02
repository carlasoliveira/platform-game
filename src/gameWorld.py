import os
import pygame

from Platform import Platform
from player import Player
class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map = [
            "11111111111111111111",
            "1..................1",
            "11111..............1",
            "1......11111111....1",
            "1..................1",
            "1.............11...1",
            "1111111............1",
            "1..................1",
            "1......1111111111111",
            "1..11..............1",
            "1..................1",
            "11111111111111111111"
        ]

        self.background = self._load_background()
        self.platforms = self._load_tiles()
        self.player_sprites = self.load_player_sprites()
        self.player = Player(
            position=pygame.math.Vector2(300, 600),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(46, 54),
            my_keys=[pygame.K_a, pygame.K_d, pygame.K_w]
        )
    


    def update(self, delta_time):
        self.player.update(delta_time)
        self.player.verify_keyboard(pygame.event.get())
        # for platform in self.platforms:
        # platform.update(delta_time, self.map)
    
    def keyboard_events(self, event):
       for event in pygame.event.get():
        self.player.verify_keyboard(event)
        
    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.player.render(self.screen)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)

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

    def load_player_sprites(self):
        base_path = os.path.dirname(__file__)
        idle_path = os.path.join(base_path, '..', 'resources', 'idle', '1.PNG')
        idle = [pygame.transform.scale(pygame.image.load(idle_path), (128, 80))]
        right = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, '..', 'resources', 'run', f'{i}.PNG')
                ), (128, 80)
            )
            for i in range(1,4)
        ]
        left = [pygame.transform.flip(img, True, False) for img in right]
        idle_left = [pygame.transform.flip(img, True, False) for img in idle]
        return [idle, idle_left, right, left]
