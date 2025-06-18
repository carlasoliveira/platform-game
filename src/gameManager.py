import pygame
from gameWorld import GameWorld 
from player import Player

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Platform Game")
        self.world = GameWorld(self.screen)
        self.player_sprites = self.world.load_player_sprites()
        self.player = Player(self.player_sprites, [300, 600], [24, 34], [0, 0])
        self.running = True
        self.last_time = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self._handle_events()
            keys = pygame.key.get_pressed()
            delta_time = self._calculate_delta_time()
            
            self.player.move(keys, self.world.map)
            self.player.update(delta_time, self.world.map)
            self._draw()
            pygame.display.update()
            self.world.clock.tick(60)
            
            
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
            
            

    def _draw(self):
        self.world.draw_background()
        self.world.draw_tiles()
        self.player.render(self.screen)
    
    def _calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time