import pygame

from Platform import Platform, Vector
from Decoration import Decoration, Vector

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
            "000002.....................cebcfgh.....1",
            "000002.........43335.....4333333335....1",
            "0000063333333337000633333700000000633330",
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
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)

                    tiles.append(Platform(position, size, img))

                if tile_char in decoration_tile_map:

                    img = pygame.transform.scale(decoration_tile_map[tile_char], (tile_size, tile_size))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)

                    tiles.append(Decoration(position, size, img))
        
        return tiles
