import pygame
from gameWorld import GameWorld
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platform Game")
        self.world = GameWorld(self.screen)
        self.running = True
        self.last_time = pygame.time.get_ticks()
        self.world._load_background_music()
        
        self.score_written = False

    def run(self):
        while self.running:
            self._handle_events()
            delta_time = self._calculate_delta_time()
            self._draw()
            if self.world.game_over:
                self.world._draw_game_over()
            elif self.world.victory_achieved:
                self.world._draw_victory()
            else:
                self.world.keyboard_events()
                self.world.update(delta_time)
                self.world.resolve_collisions()
           
            if (self.world.game_over or self.world.victory_achieved) and not self.score_written:
                self.world.write_score()
                self.score_written = True 

            pygame.display.update()
            self.world.clock.tick(60)
            

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.world.game_over or self.world.victory_achieved):
                    self._restart_game()
    def _restart_game(self):
        # Reseta o estado antes de criar um novo mundo
        if hasattr(self.world, 'reset_game_state'):
            self.world.reset_game_state()
        self.world = GameWorld(self.screen)
        self.world._load_background_music()

    def _draw(self):
        self.world.draw()

    def _calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time
