import pygame
from gameWorld import GameWorld 

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Platform Game")
        self.world = GameWorld(self.screen)
        self.running = True

    def run(self):
        while self.running:
            deltaTime = self._calculate_delta_time()
            self._handle_events()
            self._update()
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

    def _update(self):
        pass  # sem lógica de jogador por enquanto

    def _draw(self):
        self.world.draw_background()
        self.world.draw_tiles()
    
    def _calculate_delta_time(self):
        last_time = 0
        current_time = pygame.time.get_ticks()
        deltaTime = (current_time - last_time) / 1000.0
        last_time = current_time
        return deltaTime