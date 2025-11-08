from enum import Enum
import pygame
from gameWorld import GameWorld
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os

from menu import Menu
from score import Score


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

        self.clock = pygame.time.Clock() 
        self.running = True
        self.state = StateMachine.MENU
        self.last_time = pygame.time.get_ticks()
        
        # Instanciação do Menu APENAS uma vez
        self.menu = Menu()
        
        # Inicialização do mundo do jogo (será criado mais tarde, quando for INICIO)
        self.world = None 
        self.world_initialized = False # Para saber se o GameWorld já foi criado
        # Score (history) screen
        self.score = None
        self.score_initialized = False

    def run(self):
        while self.running:
            self._handle_events() 
            
            delta_time = self._calculate_delta_time()
                
            if self.state == StateMachine.INICIO:
                if not self.world_initialized:
                    self.world = GameWorld(self.screen)
                    self.world._load_background_music()
                    # Pass player names from menu into the world (if provided)
                    try:
                        # menu stores names when Start is pressed
                        if hasattr(self.menu, 'player_name_1') and self.menu.player_name_1.strip() != "":
                            self.world.player1_name = self.menu.player_name_1
                        if hasattr(self.menu, 'player_name_2') and self.menu.player_name_2.strip() != "":
                            self.world.player2_name = self.menu.player_name_2
                    except Exception:
                        pass
                    self.world_initialized = True
                    
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
                self.clock.tick(60)


    def _handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            # State-specific event delegation
            if self.state == StateMachine.MENU:
                # delegate single event to menu
                res = self.menu.handle_event(event)
                if res == 'start':
                    print('Iniciou o jogo')
                    self.state = StateMachine.INICIO
                elif res == 'history':
                    print('Abrindo histórico')
                    self.state = StateMachine.FIM
                    if not self.score_initialized:
                        self.score = Score()
                        self.score_initialized = True
                # draw menu (kept here to match previous structure)
                self.menu.draw(self.screen)
                pygame.display.update()
                self.clock.tick(60)

            elif self.state == StateMachine.FIM:
                # delegate to score screen
                if self.score is None:
                    self.score = Score()
                res = self.score.handle_event(event)
                if res == 'back':
                    self.state = StateMachine.MENU
                # draw score screen
                self.score.draw(self.screen)
                pygame.display.update()
                self.clock.tick(60)
                
    def _calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        return delta_time
