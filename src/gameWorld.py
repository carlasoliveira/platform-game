import pygame

from Platform import Platform, Vector

class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map = [
            ".......................................1",
            ".......................................1",
            "5......................................1",
            "65.....................................1",
            "02.....................................1",
            "0635...................................1",
            "000635.................................1",
            "000002.................................1",
            "000002.................................1",
            "000002.................................1",
            "000002.................................1",
            "000002.........................45......1",
            "000002.........43335........4337635....1",
            "0000063333333337000633333333700000633330",
            "0000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000"
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

        tile_map = {
            "0": self.get_sprite(self.tileset, 1, 8, 16), #tile_DIRT
            "1": self.get_sprite(self.tileset, 0, 8, 16), #tile_DIRT_EDGE_LEFT
            "2": self.get_sprite(self.tileset, 2, 8, 16), #tile_DIRT_EDGE_RIGHT
            
            "3": self.get_sprite(self.tileset, 1, 7, 16), #tile_GRASS
            "4": self.get_sprite(self.tileset, 0, 7, 16), #tile_GRASS_EDGE_LEFT
            "5": self.get_sprite(self.tileset, 2, 7, 16), #tile_GRASS_EDGE_RIGHT

            "6": self.get_sprite(self.tileset, 4, 8, 16), #tile_GRASS_EDGE_TOP_LEFT
            "7": self.get_sprite(self.tileset, 5, 8, 16), #tile_GRASS_EDGE_TOP_RIGHT
            
            #"6": self.get_sprite(self.tileset, 0, 0, 16), #tile_
            #"7": self.get_sprite(self.tileset, 0, 0, 16), #tile_
            #"8": self.get_sprite(self.tileset, 0, 0, 16), #tile_
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in tile_map:

                    img = pygame.transform.scale(tile_map[tile_char], (tile_size, tile_size))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)

                    tiles.append(Platform(position, size, img))
        return tiles
