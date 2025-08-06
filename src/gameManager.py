import pygame as pg
from gameWorld import GameWorld 
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os

class GameManager:
    def __init__(self):
<<<<<<< HEAD
        pg.init()
        self.screen = pg.display.set_mode((1280, 768))
        pg.display.set_caption("Platform Game")
=======
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platform Game")
>>>>>>> 64eb10b34a7895accab65c36d71a5d6e23a3ba59
        self.world = GameWorld(self.screen)
        self.running = True
        self.last_time = pygame.time.get_ticks()
        self.world._load_background_music()

    def run(self):
        while self.running:
            self._handle_events()
            delta_time = self._calculate_delta_time()
            self._draw()
<<<<<<< HEAD
            pg.display.update()
=======
            
            self.world.keyboard_events()
            self.world.update(delta_time)
            pygame.display.update()
>>>>>>> 64eb10b34a7895accab65c36d71a5d6e23a3ba59
            self.world.clock.tick(60)
            self.world.resolve_collisions()

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def _draw(self):
        self.world.draw()

    
    def _calculate_delta_time(self):
<<<<<<< HEAD
        last_time = 0
        current_time = pg.time.get_ticks()
        deltaTime = (current_time - last_time) / 1000.0
        last_time = current_time
        return deltaTime
=======
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time

    
>>>>>>> 64eb10b34a7895accab65c36d71a5d6e23a3ba59
