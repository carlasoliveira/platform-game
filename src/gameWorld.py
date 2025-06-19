import pygame

from Platform import Platform, Vector

class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map = [
            "1111111111111111111111111111111111111111",
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
            "1......................................1",
            "1.............11.......................1",
            "1111111.......1111.....................1",
            "1......................................1",
            "1..........................1111111111111",
            "1...............11.....11112222222222222",
            "1111111111111111111111122222222222222222",
            "2222222222222222222222222222222222222222",
            "2222222222222222222222222222222222222222"
        ]

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

    def _load_tiles(self):

        tiles = []
        tile_size = 32

        img_grass = pygame.image.load('../resources/graphics/grass.png')
        img_dirt = pygame.image.load('../resources/graphics/dirt.png')

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "1":
                    img = pygame.transform.scale(img_grass, (tile_size, tile_size))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)
                    tile = Platform(position, size, img)
                    tiles.append(tile)
                if tile == "2":
                    img = pygame.transform.scale(img_dirt, (tile_size, tile_size))
                    position = Vector(x * tile_size, y * tile_size)
                    size = Vector(tile_size, tile_size)
                    tile = Platform(position, size, img)
                    tiles.append(tile)
        return tiles
