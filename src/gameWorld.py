import pygame 

class GameWorld:
    def __init__(self, screen):
        self.screen = screen # recebe o tamanho da tela na gameManager
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
        self.screen.blit(self.background, (0, 0)) # background da tela

    def draw_tiles(self):
        for y, row in enumerate(self.map): 
            for x, tile in enumerate(row): 
                if tile != ' ':
                    img = self.tileset.get(tile) 
                    if img: 
                        self.screen.blit(img, (x * 64, y * 64))

    def _load_background(self):
        bg = pygame.image.load('../resources/graphics/background.png')
        return pygame.transform.scale(bg, (1280, 768))

    def _load_tiles(self):
        tiles = {}
        for i in range(1, 10):
            img = pygame.image.load('../resources/graphics/tile1.png')
            tiles[str(i)] = pygame.transform.scale(img, (64, 64))
        return tiles
