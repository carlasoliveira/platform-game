import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:

    def __init__(self):
        self.player_name_1 = ""
        self.player_name_2 = ""
        base_path = os.path.dirname(__file__)
        font_path = os.path.join(
            base_path, '..', 'resources', 'font', 'PotatoFont.ttf')
        self.title_font = pygame.font.Font(font_path, 74)
        self.instruction_font = pygame.font.Font(font_path, 28)
        self.start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 50)
        self.start_button_hovered = False

    def draw(self, screen):
        print('Desenhou o menu')
        
        overlay = pygame.Surface((450, 300))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (416, 235))

        title_text = self.title_font.render("MENU", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        button_color = (
            100, 200, 100) if self.start_button_hovered else (50, 150, 50)
        pygame.draw.rect(screen, button_color, self.start_button)
        pygame.draw.rect(screen, (255, 255, 255), self.start_button, 2)

        button_text = self.instruction_font.render("START", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.start_button.center)
        screen.blit(button_text, button_text_rect)
        
        quit_text = self.instruction_font.render(
            "Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(quit_text, quit_rect)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.start_button_hovered = self.start_button.collidepoint(
                    event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                return False
