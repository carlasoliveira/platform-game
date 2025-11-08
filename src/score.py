import pygame
import os
import json
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Score:

    def __init__(self):
        self.player_name_1 = ""
        self.player_name_2 = ""
        base_path = os.path.dirname(__file__)
        font_path = os.path.join(
            base_path, '..', 'resources', 'font', 'PotatoFont.ttf')
        self.title_font = pygame.font.Font(font_path, 74)
        self.instruction_font = pygame.font.Font(font_path, 28)
        # Back button for the history screen
        self.back_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 40)
        self.back_hovered = False

    def draw(self, screen):
        # clear screen for history view (only history + back button)
        screen.fill((20, 20, 30))

        # Header
        header = self.title_font.render("Historico de pontos", True, (255, 255, 255))
        header_rect = header.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(header, header_rect)

        # Draw scores list (read from resources/scores.json)
        scores = self.load_scores()
        start_x = 40
        start_y = 110
        line_h = 26
        y = start_y
        if not scores:
            empty = self.instruction_font.render("Nenhum registro encontrado.", True, (200, 200, 200))
            screen.blit(empty, (start_x, y))
        else:
            # show most recent first, limit to 12
            recent = list(reversed(scores))[:12]
            for entry in recent:
                ts = entry.get('timestamp', '')
                reason = entry.get('reason', '')
                p1 = entry.get('player1', {})
                p2 = entry.get('player2', {})
                line1 = f"{ts} - {reason}"
                line2 = f"{p1.get('name','')} : {p1.get('score','0')}    {p2.get('name','')} : {p2.get('score','0')}"
                t1 = self.instruction_font.render(line1, True, (220, 220, 220))
                t2 = self.instruction_font.render(line2, True, (200, 200, 200))
                screen.blit(t1, (start_x, y))
                screen.blit(t2, (start_x, y + 18))
                y += line_h * 2

        # back button
        back_color = (100, 200, 100) if self.back_hovered else (50, 150, 50)
        pygame.draw.rect(screen, back_color, self.back_button)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button, 2)
        back_text = self.instruction_font.render("Voltar", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

    def handle_event(self, event):
        # Handle a single event delegated by GameManager
        if event.type == pygame.MOUSEMOTION:
            self.back_hovered = self.back_button.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return 'back'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        return False

    def load_scores(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, '..', 'resources', 'scores.json')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            if isinstance(data, list):
                    return data
            else:
                    return [data]  

        return []
