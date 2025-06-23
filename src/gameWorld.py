import pygame

from Platform import Platform, Vector

class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map = [
            "111111111111111111111111111111111111111",
            "1......................................1",
            "11111..................................1",
            "1......................................1",
            "1......................................1",
            "1.............11.......................1",
            "1111111.......1111.....................1",
            "1......................................1",
            "1..........................1111111111111",
            "1...................11.................1",
            "1111111111111111111111111111111111111111",
            "2222222222222222222222222222222222222222",
            "1......................................1",
            "11111..................................1",
            "1......................................1",
            "1......................................1"
        ]

        self.tileset = pygame.image.load('../resources/graphics/tileset.png').convert_alpha()
        self.background = self._load_background()
        self.platforms = self._load_tiles()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)

    def _load_background(self):
        bg = pygame.image.load('../resources/graphics/background.png')
        return pygame.transform.scale(bg, (1280, 768))

    def get_sprite(self, sheet, col, row, size):
        rect = pygame.Rect(col * size, row * size, size, size)
        return sheet.subsurface(rect).copy()

    def _load_tiles(self):

        tiles = []
        tile_size = 32

        sprite_grass = self.get_sprite(self.tileset, 1, 3, 16)  # coluna 0, linha 3
        sprite_dirt = self.get_sprite(self.tileset, 1, 4, 16)  # coluna 1, linha 3

        print(f"sprite_grass: {sprite_grass.get_size()}")

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "1":
                    img = pygame.transform.scale(sprite_grass, (32,32))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)
                    tile = Platform(position, size, img)
                    tiles.append(tile)
                if tile == "2":
                    img = pygame.transform.scale(sprite_dirt, (32,32))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)
                    tile = Platform(position, size, img)
                    tiles.append(tile)
        return tiles
