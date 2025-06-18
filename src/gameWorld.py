import pygame 
import os
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
        self.tileset = self._load_tiles()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for y, row in enumerate(self.map): 
            for x, tile in enumerate(row): 
                if tile != ' ':
                    img = self.tileset.get(tile) 
                    if img: 
                        self.screen.blit(img, (x * 64, y * 64))

    def _load_background(self):
        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, '..', 'resources', 'graphics', 'background.png')
        bg = pygame.image.load(bg_path)
        return pygame.transform.scale(bg, (1280, 768))

    def _load_tiles(self):
        tiles = {}
        for i in range(1, 10):
            base_path = os.path.dirname(__file__)
            tile_path = os.path.join(base_path, '..', 'resources', 'graphics', 'tile1.png')
            img = pygame.image.load(tile_path)
            tiles[str(i)] = pygame.transform.scale(img, (64, 64))
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
