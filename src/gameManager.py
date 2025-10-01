from enum import Enum
import pygame
from gameWorld import GameWorld
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os

from menu import Menu


class StateMachine(Enum):
    MENU = 1
    INICIO = 2
    FIM = 3


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platform Game")
        self.start_game = False
        self.running = True
        self.state = StateMachine.MENU
        self.last_time = pygame.time.get_ticks()

    def run(self):
        while self.running:
            # self._handle_events()

            if self.state == StateMachine.MENU:
                print('No estado menu')
                self.menu = Menu()
                self.menu.draw(self.screen)
                
                if self.menu.handle_event():
                    print('Iniciou o jogo')
                    self.state = StateMachine.INICIO
            if self.state == StateMachine.INICIO:
                self.world = GameWorld(self.screen)
                self.world._load_background_music()
                delta_time = self._calculate_delta_time()
                if self.world.game_over:
                    self.world._draw_game_over()
                elif self.world.victory_achieved:
                    self.world._draw_victory()
                else:
                    self.world.keyboard_events()
                    self.world.update(delta_time)
                    self.world.resolve_collisions()
                    self.world.draw()
                pygame.display.update()
                self.world.clock.tick(60)


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # elif event.key == pygame.K_r and (self.world.game_over or self.world.victory_achieved):
                #     self._restart_game()

    # def _restart_game(self):
    #     if hasattr(self.world, 'reset_game_state'):
    #         self.world.reset_game_state()
    #     self.world = GameWorld(self.screen)
    #     self.world._load_background_music()


    def _calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time
