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
        # Move start button a bit lower to add spacing from input boxes
        self.start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        self.start_button_hovered = False
        # History button below start
        self.history_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, self.start_button.y + self.start_button.height + 12, 200, 40)
        self.history_button_hovered = False

        self.input_boxes = [pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 120, 300, 36),
                            pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 60, 300, 36)]
        self.active_input = None
        self.input_texts = ["", ""]
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.text_color = pygame.Color('white')

    def draw(self, screen):
        # clear background so menu is visible
        screen.fill((30, 30, 50))
        # semi-transparent overlay
        overlay = pygame.Surface((500, 360), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 180))

        # title
        title_text = self.title_font.render("MENU", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        # start button
        button_color = (100, 200, 100) if self.start_button_hovered else (50, 150, 50)
        pygame.draw.rect(screen, button_color, self.start_button)
        pygame.draw.rect(screen, (255, 255, 255), self.start_button, 2)
        button_text = self.instruction_font.render("START", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.start_button.center)
        screen.blit(button_text, button_text_rect)

        # history button
        hist_color = (120, 120, 200) if self.history_button_hovered else (80, 80, 140)
        pygame.draw.rect(screen, hist_color, self.history_button)
        pygame.draw.rect(screen, (255, 255, 255), self.history_button, 2)
        hist_text = self.instruction_font.render("HISTORICO DE PONTOS", True, (255, 255, 255))
        hist_rect = hist_text.get_rect(center=self.history_button.center)
        screen.blit(hist_text, hist_rect)

        # quit instruction
        quit_text = self.instruction_font.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT + 10// 2 + 100))
        screen.blit(quit_text, quit_rect)

        # Draw input boxes labels and boxes
        label1 = self.instruction_font.render("Player 1 name:", True, (220, 220, 220))
        label2 = self.instruction_font.render("Player 2 name:", True, (220, 220, 220))
        screen.blit(label1, (self.input_boxes[0].x, self.input_boxes[0].y - 26))
        screen.blit(label2, (self.input_boxes[1].x, self.input_boxes[1].y - 26))

        for i, rect in enumerate(self.input_boxes):
            color = self.color_active if self.active_input == i else self.color_inactive
            pygame.draw.rect(screen, (50, 50, 70), rect)
            pygame.draw.rect(screen, color, rect, 2)
            # render text
            txt_surf = self.instruction_font.render(self.input_texts[i], True, self.text_color)
            screen.blit(txt_surf, (rect.x + 8, rect.y + 6))

    def handle_event(self, event):
        # Mouse movement: hover start button
        if event.type == pygame.MOUSEMOTION:
            self.start_button_hovered = self.start_button.collidepoint(event.pos)
            self.history_button_hovered = self.history_button.collidepoint(event.pos)

        # Mouse click: select input or click start
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check inputs
            clicked_input = None
            for i, rect in enumerate(self.input_boxes):
                if rect.collidepoint(event.pos):
                    clicked_input = i
                    break
            self.active_input = clicked_input

            # start button click (left button)
            if event.button == 1 and self.start_button.collidepoint(event.pos):
                # only start if both names are non-empty
                if self.input_texts[0].strip() != "" and self.input_texts[1].strip() != "":
                    # store into player_name fields
                    self.player_name_1 = self.input_texts[0].strip()
                    self.player_name_2 = self.input_texts[1].strip()
                    return 'start'
                else:
                    return False

            # history button click
            if event.button == 1 and self.history_button.collidepoint(event.pos):
                return 'history'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if self.active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    self.input_texts[self.active_input] = self.input_texts[self.active_input][:-1]
                elif event.key == pygame.K_RETURN:
                    if self.active_input == 0:
                        self.active_input = 1
                    else:
                        self.active_input = None
                else:
                    if len(self.input_texts[self.active_input]) < 20:
                        self.input_texts[self.active_input] += event.unicode

        return False



