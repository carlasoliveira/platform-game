import pygame
from gameWorld import GameWorld 

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 768))
        pygame.display.set_caption("Platform Game")
        self.world = GameWorld(self.screen)
        self.running = True
        self.last_time = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self._handle_events()
            delta_time = self._calculate_delta_time()
            self._draw()
            
            # Verifica o teclado a cada frame, não apenas em eventos
            self.world.keyboard_events()
            self.world.update(delta_time)
            pygame.display.update()
            self.world.clock.tick(60)
            self.world.resolve_collisions()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _draw(self):
        self.world.draw()
        self.world.player.render(self.screen)

    
    def _calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time