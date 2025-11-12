import os
import pygame

from animated_gif import AnimatedGif
from collider import Collider
from collectible import Collectible
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_SPEED, JUMP_SPEED
from decoration import Decoration
from lava import Lava
from Platform import Platform
from player import Player
from puzze import Puzze, PuzzleType, PressurePlate
from controlledBlock import ControlledBlock, ControlledBlockType
from secretArea import SecretArea

LEVEL = 2

class GameWorld:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Selecionar mapa principal com base na variável global LEVEL
        self.map = self.mapSelect()

        # Selecionar mapa controlado com base na variável global LEVEL
        self.controlled_map = self.mapControlledSelect()

        self.background = self._load_background()
        self.tileset = self._load_tileset()
        self.platforms = self._load_platforms()
        self.decorations = self._load_decorations()
        self.doors = self._load_doors()  # Portas separadas para controle especial
        self.collectibles = self._load_collectibles()
        self.puzzles = self._load_puzzles()
        self.lavas = self._load_lava()
        self.secret_areas = self._load_secret_areas()  # Carrega áreas secretas
        self.pressure_plates = self._load_pressure_plates()  # Carrega placas de pressão
        self.controlled_blocks = self._load_controlled_blocks()  # Carrega blocos controlados
        self.player_sprites = self.load_player_sprites()
        self.player_sprites2 = self.load_player_sprites2()
        self._load_background_music()
        self.collider = Collider()
        self.game_over = False
        self.has_key = False  # Variável para registrar se a chave foi coletada

        # Variáveis para controle da porta
        self.door_opening = False  # Flag para indicar se a porta está sendo aberta
        self.door_open_timer = 0.0  # Timer para delay de abertura da porta
        self.door_open_delay = 0.3  # Delay de 0.3s para abrir a porta

        # Variáveis para detecção de vitória
        self.both_players_at_door_timer = 0.0  # Timer para ambos jogadores na porta
        self.victory_timer_threshold = 1.5  # 1.5 segundos para vitória
        self.victory_achieved = False  # Flag de vitória

        # Lista para plataformas criadas dinamicamente (caixas que caíram na lava)
        self.dynamic_platforms = []

        # Carrega sons
        self._load_door_sound()
        # Som de bloco em movimento/controle
        self._load_moving_block_sound()

        # Inicializar posições dos jogadores a partir do mapping por LEVEL
        spawn1, spawn2 = self.spawnSelect()

        self.player1 = Player(
            position=pygame.math.Vector2(spawn1[0], spawn1[1]),
            sprites=self.player_sprites2,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),
            my_keys=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
            player_type="player1"
        )

        self.player2 = Player(
            position=pygame.math.Vector2(spawn2[0], spawn2[1]),
            sprites=self.player_sprites,
            velocity=pygame.math.Vector2(0, 0),
            size=pygame.math.Vector2(24, 40),
            my_keys=[pygame.K_a, pygame.K_d, pygame.K_w],
            player_type="player2"
        )

        base_path = os.path.dirname(__file__)
        font_path = os.path.join(
            base_path, '..', 'resources', 'font', 'PotatoFont.ttf')
        self.font = pygame.font.Font(font_path, 36)
        self.title_font = pygame.font.Font(font_path, 74)
        self.subtitle_font = pygame.font.Font(font_path, 36)
        self.instruction_font = pygame.font.Font(font_path, 28)

    def resolve_collisions(self):

        # Combina plataformas estáticas com as dinâmicas e blocos controlados sólidos
        all_platforms = self.platforms + self.dynamic_platforms
        
        # Adicionar blocos controlados que estão sólidos
        for controlled_block in self.controlled_blocks:
            if controlled_block.is_solid_collision():
                all_platforms.append(controlled_block)

        self.collider.resolve_collision(self.player1, all_platforms)
        self.collider.resolve_collision(self.player2, all_platforms)

        key_collected1 = self.collider.check_collectible_collision(
            self.player1, self.collectibles)
        key_collected2 = self.collider.check_collectible_collision(
            self.player2, self.collectibles)

        # Atualiza o estado da chave se algum jogador coletou
        if key_collected1 or key_collected2:
            self.has_key = True

        self.collider.check_puzzle_collision(self.player1, self.puzzles)
        self.collider.check_puzzle_collision(self.player2, self.puzzles)

        # Física dos puzzles
        self.collider.resolve_puzzle_physics(self.puzzles, self.platforms)
        self.collider.resolve_collision_between_puzzles(self.puzzles)

        # Verifica colisão com portas e abre se tiver chave
        self._check_door_interactions()

        game_over1 = self.collider.resolve_lava_collision(
            self.player1, self.lavas)
        game_over2 = self.collider.resolve_lava_collision(
            self.player2, self.lavas)
        self.game_over = game_over1 or game_over2

        self.collider.resolve_puzzle_physics(self.puzzles, all_platforms)

        # Verifica se alguma caixa (puzzle) caiu na lava
        self._check_puzzle_lava_collision()

    # === Selectors baseados em LEVEL ===
    def mapSelect(self):

        if(LEVEL == 1):
            return [
                "2..................................40000",
                "2.................................470000",
                "2........#.......................4700000",
                "2................................1000000",
                "2.....%...@..........!...........100YY00",
                "2...........HI...................10Z(.X0",
                "2...........FG...................XZ.)..1",
                "2........d.wDE../...$..a./.....B.....K.1",
                "2s...W33333333333333333333335.b........1",
                "65....XYYYY00000000000000000633335L43337",
                "02.........XYYYYYYYYYYYYYY00000000000000",
                "02e.......................XY000000YYYY00",
                "065.........................1000YZ....X0",
                "002b.........B.......%.......XYZ.......1",
                "0065a......a.cb.....................awe1",
                "000635....W333333U..........B......W3330",
                "00YYYZ....XYYYYYZ....bd.e....a......XYY0",
                "0Z..................43335..4335d.......1",
                "2...................XYYYZ..XYYYU.......1",
                "2......................................1",
                "2as.........*......................f...1",
                "635.............f...ab.........a..433337",
                "002d........w..43333335..bse.43333700000",
                "00635LLLLLL43337000000633333370000000000",
        ]

        if(LEVEL == 2):
            return [
                "0000000000000000000000000000000000000000",
                "00d777777777777777777c000d777777777777c0",
                "005...<........<.....40005.....<......40",
                "005.....@...#........67778......-...wp40",
                "005..........................X.....^..40",
                "005..............HI...................40",
                "005..B...........FG......~.j.....¨s...40",
                "005..............DE....pp..p.´K.|.....40",
                "00b22223......122222222222222222222222a0",
                "0d777778......6777777777777c000000000000",
                "05..<...............<......6777777777c00",
                "05.....................V.............6c0",
                "05..%.........................l.......40",
                "05!.................k........~.13.....40",
                "05................mJ....s......45.....40",
                "0b222223........1222222223..122ab223..40",
                "00P77778........6777777778..670d7778..40",
                "00S..z..................z....pR5......40",
                "00S........................:..R5w....p40",
                "00S..........ç.......w...&....R5p..:..40",
                "00Sx........*).....y*/...;....R5/.s...40",
                "00NU....*.( TQU...*TU)&p).)&.*R5..p...40",
                "000NQQQQQQQQM0SLLLTMNQQQQQQQQQMb223...40",
                "00000000000000NQQQM000000000000000b222a0",
            ]

    def mapControlledSelect(self):

        if(LEVEL == 2):
            return [
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                "........h...............................",
                "........i3..............................",
                "........4b3.............................",
                "........40b3...................WX.......",
                "........400b3..................YZ.......",
                "........4000b3..........................",
                "........40000b3...................Q.....",
                "........400000b3....................AB..",
                "........67777778....................CD..",
                "........................................",
                "........................................",
                "........................................",
                "........................................",
                ".....P..................................",
                "........................................",
                "........................................",
            ]
        return []

    def spawnSelect(self):

        if(LEVEL == 1):
            return (650, 620), (568, 620)

        if(LEVEL == 2):
            return (120, 420), (180, 420)

    def _check_door_interactions(self):
        """Verifica se algum jogador tocou na porta e abre se tiver a chave"""
        if self.has_key and not self.door_opening:
            # Verifica se alguma porta foi tocada
            door_touched = False
            for door in self.doors:
                # Verifica colisão do player1 com qualquer parte da porta
                colliding1, _ = self.collider.check_collider(
                    door, self.player1)
                # Verifica colisão do player2 com qualquer parte da porta
                colliding2, _ = self.collider.check_collider(
                    door, self.player2)

                if (colliding1 or colliding2) and not door.get_is_open():
                    door_touched = True
                    break

            # Se alguma parte da porta foi tocada, inicia o processo de abertura
            if door_touched:
                # Toca o som
                if self.door_sound:
                    self.door_sound.play()

                # Inicia o timer de abertura
                self.door_opening = True
                self.door_open_timer = 0.0
                print("Porta sendo aberta com a chave...")

    def _check_puzzle_lava_collision(self):
        """Verifica se alguma caixa caiu na lava e a converte em plataforma"""
        puzzles_to_remove = []

        for puzzle in self.puzzles:
            for lava in self.lavas:
                # Verifica se a caixa está colidindo com a lava
                colliding, _ = self.collider.check_collider(puzzle, lava)
                if colliding:
                    # Usa a posição da lava para alinhar perfeitamente a plataforma
                    lava_pos = lava.get_position()
                    lava_size = lava.get_size()

                    # Cria uma versão queimada da imagem da caixa
                    if hasattr(puzzle, 'm_image') and puzzle.m_image is not None:
                        # Cria uma cópia da imagem da caixa
                        burned_image = puzzle.m_image.copy()

                        # Cria uma superfície escura para simular queimadura
                        dark_overlay = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        dark_overlay.set_alpha(100)  # Semi-transparente
                        dark_overlay.fill((0, 0, 0))  # Preto

                        # Aplica o overlay escuro por cima da imagem original
                        burned_image.blit(dark_overlay, (0, 0))
                        platform_img = burned_image
                    else:
                        # Fallback para sprite de terra se não tiver imagem
                        platform_sprite = self.get_sprite(
                            self.tileset, 1, 8, 16)
                        platform_img = pygame.transform.scale(
                            platform_sprite, (TILE_SIZE, TILE_SIZE))

                    # Cria a nova plataforma na posição da lava para perfeito alinhamento
                    new_platform = Platform(lava_pos, lava_size, platform_img)
                    self.dynamic_platforms.append(new_platform)

                    # Remove a caixa da lista de puzzles
                    puzzles_to_remove.append(puzzle)
                    break  # Sai do loop da lava para este puzzle

        # Remove as caixas que caíram na lava
        for puzzle in puzzles_to_remove:
            if puzzle in self.puzzles:
                self.puzzles.remove(puzzle)

    def _check_victory_condition(self, delta_time):
        """Verifica se ambos jogadores estão na porta aberta por 1.5s"""
        # Primeiro verifica se pelo menos uma porta está aberta
        any_door_open = any(door.get_is_open() for door in self.doors)

        if not any_door_open:
            self.both_players_at_door_timer = 0.0
            return

        # Verifica se ambos jogadores estão tocando em qualquer porta aberta
        player1_at_door = False
        player2_at_door = False

        for door in self.doors:
            if door.get_is_open():
                colliding1, _ = self.collider.check_collider(
                    door, self.player1)
                colliding2, _ = self.collider.check_collider(
                    door, self.player2)

                if colliding1:
                    player1_at_door = True
                if colliding2:
                    player2_at_door = True

        # Verifica se ambos jogadores estão no chão (não pulando)
        player1_on_ground = self.player1.m_is_on_ground
        player2_on_ground = self.player2.m_is_on_ground

        # Se ambos estão na porta e no chão, incrementa o timer
        if player1_at_door and player2_at_door and player1_on_ground and player2_on_ground:
            self.both_players_at_door_timer += delta_time

            if self.both_players_at_door_timer >= self.victory_timer_threshold:
                self.victory_achieved = True
                print("Vitoria! !")
        else:
            # Reset o timer se a condição não for atendida
            self.both_players_at_door_timer = 0.0

    def reset_game_state(self):
        """Reseta o estado do jogo, incluindo chave e portas"""
        self.has_key = False
        self.door_opening = False
        self.door_open_timer = 0.0
        self.both_players_at_door_timer = 0.0
        self.victory_achieved = False

        # Fecha todas as portas
        for door in self.doors:
            door.close_door()

    def update(self, delta_time):
        self.player1.update(delta_time)
        self.player2.update(delta_time)

        for puzzle in self.puzzles:
            puzzle.update(delta_time)

        # Update lava animations
        delta_time_ms = delta_time * 1000  # Convert seconds to milliseconds
        for lava in self.lavas:
            lava.update(delta_time_ms)

        # Atualizar áreas secretas baseado na posição dos players
        for secret_area in self.secret_areas:
            # Verificar collision com ambos os players
            player1_pos = self.player1.get_position()
            player1_size = self.player1.get_size()
            player1_rect = pygame.Rect(player1_pos.x, player1_pos.y, 
                                     player1_size.x, player1_size.y)
            
            player2_pos = self.player2.get_position()
            player2_size = self.player2.get_size()
            player2_rect = pygame.Rect(player2_pos.x, player2_pos.y,
                                     player2_size.x, player2_size.y)
            
            # Atualizar baseado se qualquer player está na área
            player1_in_area = secret_area.check_player_collision(player1_rect)
            player2_in_area = secret_area.check_player_collision(player2_rect)
            
            # Se qualquer player estiver na área, ela deve ficar semi-transparente (50%)
            if player1_in_area or player2_in_area:
                secret_area.is_visible = True
                secret_area.alpha = max(100, secret_area.alpha - 15)
            else:
                secret_area.is_visible = True
                secret_area.alpha = min(255, secret_area.alpha + 15)

        # Atualizar placas de pressão
        self._update_pressure_plates()

        # Atualiza timer de abertura da porta
        if self.door_opening:
            self.door_open_timer += delta_time
            if self.door_open_timer >= self.door_open_delay:
                # Abre todas as portas após o delay
                for door in self.doors:
                    if not door.get_is_open():
                        door.open_door()
                self.door_opening = False
                self.door_open_timer = 0.0

        # Verifica se ambos jogadores estão na porta (quando ela estiver aberta)
        if self.has_key and not self.victory_achieved:
            self._check_victory_condition(delta_time)

    def keyboard_events(self):
        self.player1.verify_keyboard()
        self.player2.verify_keyboard()

    def _update_pressure_plates(self):
        """Atualiza o estado das placas de pressão e blocos controlados"""
        # Criar lista de objetos que podem ativar placas (players + puzzles móveis)
        activating_objects = [self.player1, self.player2]
        
        # Adicionar blocos móveis que podem ativar placas
        for puzzle in self.puzzles:
            if puzzle.get_puzzle_type() == PuzzleType.MOVABLE_BLOCK:
                activating_objects.append(puzzle)
        
        # Verificar cada placa de pressão
        for plate in self.pressure_plates:
            state_changed = plate.check_activation(activating_objects)
            
            if state_changed:
                # Se o estado mudou, atualizar blocos controlados
                self._update_controlled_blocks_for_plate(plate.get_plate_id(), plate.is_active())
                # Tocar som de bloco/movimento quando a placa muda de estado (ativa/desativa)
                try:
                    if hasattr(self, 'moving_block_sound') and self.moving_block_sound:
                        self.moving_block_sound.play()
                except Exception:
                    pass
    
    def _update_controlled_blocks_for_plate(self, plate_id, is_active):
        """Atualiza blocos controlados por uma placa específica"""
        for block in self.controlled_blocks:
            if block.get_pressure_plate_id() == plate_id:
                block.set_pressure_plate_state(is_active)

    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_score()
        self.player1.render(self.screen)
        self.player2.render(self.screen)
        
        # Renderizar áreas secretas por último (para sobrepor tudo, incluindo players)
        for secret_area in self.secret_areas:
            secret_area.render(self.screen)

        # Desenha popup de vitória se necessário
        if self.victory_achieved:
            self._draw_victory()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_tiles(self):
        for platform in self.platforms:
            platform.render(self.screen)
        # Renderiza plataformas dinâmicas antes da lava (para aparecer através da transparência)
        for platform in self.dynamic_platforms:
            platform.render(self.screen)
        # Renderiza lava por cima (com transparência)
        for lava in self.lavas:
            lava.render(self.screen)
        for decoration in self.decorations:
            decoration.render(self.screen)
        for door in self.doors:
            door.render(self.screen)
        for collectible in self.collectibles:
            collectible.render(self.screen)
        for puzzle in self.puzzles:
            puzzle.render(self.screen)
        for pressure_plate in self.pressure_plates:
            pressure_plate.render(self.screen)
        for controlled_block in self.controlled_blocks:
            controlled_block.render(self.screen)

    def draw_score(self):
        score1_text = self.font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        self.screen.blit(score1_text, (10, 10))

        score2_text = self.font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        self.screen.blit(score2_text, (10, 50))

        # Desenha indicador de chave
        if self.has_key:
            key_text = self.font.render("CHAVE COLETADA!", True, (255, 255, 0))
            self.screen.blit(key_text, (10, 90))

        # Desenha barra de progresso para vitória
        if self.both_players_at_door_timer > 0 and not self.victory_achieved:
            progress = min(self.both_players_at_door_timer /
                           self.victory_timer_threshold, 1.0)
            self._draw_victory_progress(progress)

    def _draw_victory_progress(self, progress):
        """Desenha barra de progresso para vitória"""
        # Texto indicativo
        progress_text = self.instruction_font.render(
            "Ambos na porta! Aguarde...", True, (255, 255, 0))
        text_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(progress_text, text_rect)

        # Barra de progresso
        bar_width = 300
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 170

        # Fundo da barra
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (100, 100, 100), background_rect)

        # Progresso da barra
        progress_width = int(bar_width * progress)
        progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
        color = (255, 255 - int(progress * 255), 0)  # Amarelo para verde
        pygame.draw.rect(self.screen, color, progress_rect)

        # Borda da barra
        pygame.draw.rect(self.screen, (255, 255, 255), background_rect, 2)

    def _draw_game_over(self):
        overlay = pygame.Surface((450, 300))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (416, 235))

        # Texto principal "GAME OVER"
        title_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # Texto de pontuação
        score1_text = self.subtitle_font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        score1_rect = score1_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score1_text, score1_rect)

        score2_text = self.subtitle_font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        score2_rect = score2_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score2_text, score2_rect)

        # Instruções para reiniciar
        restart_text = self.instruction_font.render(
            "Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, restart_rect)

        # Instruções para sair
        quit_text = self.instruction_font.render(
            "Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(quit_text, quit_rect)

    def _draw_victory(self):
        """Desenha a tela de vitória"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 50, 0))  # Verde escuro para vitória
        self.screen.blit(overlay, (0, 0))

        # Texto principal "!"
        title_text = self.title_font.render("VITORIA!", True, (50, 255, 50))
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # Texto de fase completada
        stage_text = self.subtitle_font.render(
            "Fase Completada!", True, (255, 255, 255))
        stage_rect = stage_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(stage_text, stage_rect)

        # Texto de pontuação final
        score1_text = self.instruction_font.render(
            f"Pastor (Brancas): {self.player1.get_score()}", True, (255, 255, 255))
        score1_rect = score1_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score1_text, score1_rect)

        score2_text = self.instruction_font.render(
            f"Pastor (Pretas): {self.player2.get_score()}", True, (255, 255, 255))
        score2_rect = score2_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(score2_text, score2_rect)

        # Instruções para continuar
        restart_text = self.instruction_font.render(
            "Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

        # Instruções para sair
        quit_text = self.instruction_font.render(
            "Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
        self.screen.blit(quit_text, quit_rect)

    def _load_background(self):
        base_path = os.path.dirname(__file__)

        if(LEVEL == 1):
            bg_path = os.path.join(base_path, '..', 'resources',
                                'graphics', 'background.png')
        if(LEVEL == 2):
            bg_path = os.path.join(base_path, '..', 'resources',
                                'graphics', 'background2.png')
        bg = pygame.image.load(bg_path)
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def _load_tileset(self):
        base_path = os.path.dirname(__file__)
        tileset_path = os.path.join(
            base_path, '..', 'resources', 'graphics', 'tile1.png')
        tileset = pygame.image.load(tileset_path)
        return tileset

    def get_sprite(self, tileset, x, y, tile_size):
        sprite = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        sprite.blit(tileset, (0, 0), (x * tile_size,
                    y * tile_size, tile_size, tile_size))
        return sprite

    def _load_collectibles(self):
        from collectible import CollectibleType
        collectibles = []
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "w":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(
                        position, size, CollectibleType.WHITE_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "s":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(24, 24)
                    collectible = Collectible(
                        position, size, CollectibleType.BLACK_SHEEP, points=10)
                    collectibles.append(collectible)
                elif tile == "K":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE + 4, y * TILE_SIZE + 4)
                    size = pygame.math.Vector2(28, 28)
                    collectible = Collectible(
                        position, size, CollectibleType.KEY, points=0)
                    collectibles.append(collectible)
        return collectibles

    def _load_secret_areas(self):
        secret_areas = []
            
        if(LEVEL == 2):
            
            #secret_areas.append(SecretArea(50, 489, 920, 255, '#0F0B0D'))
            secret_areas.append(SecretArea(1000, 340, 227, 157, '#0F0B0D'))
            secret_areas.append(SecretArea(1010, 490, 217, 255, '#0F0B0D')) 
            
        return secret_areas

    def _load_pressure_plates(self):

        pressure_plates = []
            
        if(LEVEL == 2):

            sprite_inactive = self.get_sprite(self.tileset, 30, 2, 16)
            sprite_active = self.get_sprite(self.tileset, 31, 2, 16)
            
            plate_chars = {

                'P': 'plate1',
                'Q': 'plate2'
            }
        
        # Percorrer matriz e criar placas
        for y, row in enumerate(self.controlled_map):
            for x, char in enumerate(row):
                if char in plate_chars:
                    plate_id = plate_chars[char]
                    position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    
                    plate = PressurePlate(
                        position=position,
                        size=pygame.math.Vector2(TILE_SIZE, TILE_SIZE),
                        plate_id=plate_id,
                        sprite_inactive=sprite_inactive,
                        sprite_active=sprite_active
                    )
                    pressure_plates.append(plate)
                    print(f"Placa '{plate_id}' criada em ({x}, {y}) = pos({position.x}, {position.y})")
        
        return pressure_plates

    def _load_controlled_blocks(self):
        """Carrega blocos controlados da matriz controlled_map"""
        controlled_blocks = []
            
        if(LEVEL == 2):

            block_chars = {
            
                "0": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (1, 40)), # tile_DIRT

                "3": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (2, 39)), # tile_WOODS_TOP_RIGHT
                "4": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (0, 40)), # tile_WOODS_MID_LEFT

                "6": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (0, 41)), # tile_WOODS_BOT_LEFT
                "7": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (1, 41)), # tile_WOODS_BOT_CENTER
                "8": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (2, 41)), # tile_WOODS_BOT_RIGHT

                "b": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (20, 40)), # tile_WOODS_CORNER_TOP_RIGHT
                "h": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (23, 40)), # tile_WOODS_STAIRS_AJUST-1
                "i": ('plate1', ControlledBlockType.APPEAR_WHEN_ACTIVE, (23, 41)), # tile_WOODS_STAIRS_AJUST-2

                "W": ('plate1', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (0, 39)), # tile_WOODS_TOP_LEFT
                "X": ('plate1', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (2, 39)), # tile_WOODS_TOP_RIGHT
                "Y": ('plate1', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (0, 41)), # tile_WOODS_BOT_LEFT
                "Z": ('plate1', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (2, 41)), # tile_WOODS_BOT_RIGHT

                "A": ('plate2', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (0, 39)), # tile_WOODS_TOP_LEFT
                "B": ('plate2', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (2, 39)), # tile_WOODS_TOP_RIGHT
                "C": ('plate2', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (0, 41)), # tile_WOODS_BOT_LEFT
                "D": ('plate2', ControlledBlockType.DISAPPEAR_WHEN_ACTIVE, (2, 41)), # tile_WOODS_BOT_RIGHT
            }
        
        # Percorrer matriz e criar blocos controlados
        for y, row in enumerate(self.controlled_map):
            for x, char in enumerate(row):
                if char in block_chars:
                    plate_id, block_type, sprite_coords = block_chars[char]
                    position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    
                    # Extrair sprite específico para este caractere
                    sprite_x, sprite_y = sprite_coords
                    block_sprite = self.get_sprite(self.tileset, sprite_x, sprite_y, 16)
                    
                    block = ControlledBlock(
                        position=position,
                        size=pygame.math.Vector2(TILE_SIZE, TILE_SIZE),
                        pressure_plate_id=plate_id,
                        block_type=block_type,
                        sprite_normal=block_sprite
                    )
                    controlled_blocks.append(block)
                    
                    behavior = "aparece" if "APPEAR" in block_type else "desaparece"
                    print(f"Bloco '{char}' criado em ({x}, {y}) = pos({position.x}, {position.y}) | Placa: {plate_id} | {behavior} | Sprite: ({sprite_x}, {sprite_y})")
        
        return controlled_blocks

    def _load_lava(self):
        lavas = []

        # Try to load animated gif first
        try:
            lava_gif_path = os.path.join("resources", "graphics", "lava.gif")
            lava_animated_gif = AnimatedGif(
                lava_gif_path, scale_size=(TILE_SIZE, TILE_SIZE))
        except:
            lava_animated_gif = None

        # Fallback to tileset sprite
        pixel = self.get_sprite(self.tileset, 1, 46, 8)

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "L":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)

                    if lava_animated_gif:
                        # Create lava with animated gif
                        lava = Lava(position, size, None, lava_animated_gif)
                    else:
                        # Fallback to static image
                        img = pygame.transform.scale(
                            pixel, (TILE_SIZE, TILE_SIZE))
                        lava = Lava(position, size, img, None)

                    lavas.append(lava)
        return lavas

    def _load_puzzles(self):
        puzzles = []
        
        # Carrega a textura da caixa
        try:
            box_image = pygame.image.load(os.path.join("resources", "graphics", "obstaculo.png"))
            box_image = pygame.transform.scale(box_image, (TILE_SIZE, TILE_SIZE))
        except:
            # Fallback para sprite do tileset se não conseguir carregar a imagem
            box_sprite = self.get_sprite(self.tileset, 1, 8, 16)
            box_image = pygame.transform.scale(box_sprite, (TILE_SIZE, TILE_SIZE))

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == "B":
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    velocity = pygame.math.Vector2(0, 0)
                    puzzle = Puzze(position, size, velocity,
                                   PuzzleType.MOVABLE_BLOCK, box_image)
                    puzzles.append(puzzle)
        return puzzles

    def _load_platforms(self):
        platforms = []

        if(LEVEL == 1):
            plataform_tile_map = {
                "0": self.get_sprite(self.tileset, 1, 8, 16), # tile_DIRT
                "1": self.get_sprite(self.tileset, 0, 8, 16), # tile_DIRT_EDGE_LEFT
                "2": self.get_sprite(self.tileset, 2, 8, 16), # tile_DIRT_EDGE_RIGHT

                "3": self.get_sprite(self.tileset, 1, 7, 16), # tile_GRASS
                "4": self.get_sprite(self.tileset, 0, 7, 16), # tile_GRASS_EDGE_LEFT
                "5": self.get_sprite(self.tileset, 2, 7, 16), # tile_GRASS_EDGE_RIGHT

                "W": self.get_sprite(self.tileset, 0, 10, 16), # tile_ONLY_GRASS_LEFT
                "U": self.get_sprite(self.tileset, 2, 10, 16), # tile_ONLY_GRASS_RIGHT
                "V": self.get_sprite(self.tileset, 1, 10, 16), # tile_ONLY_GRASS_CENTER

                
                "6": self.get_sprite(self.tileset, 4, 8, 16), # tile_GRASS_EDGE_TOP_RIGHT
                "7": self.get_sprite(self.tileset, 5, 8, 16), # tile_GRASS_EDGE_TOP_LEFT

                "X": self.get_sprite(self.tileset, 0, 9, 16), # tile_DIRT_BOTTOM_LEFT
                "Y": self.get_sprite(self.tileset, 1, 9, 16), # tile_DIRT_BOTTOM
                "Z": self.get_sprite(self.tileset, 2, 9, 16), # tile_DIRT_BOTTOM_right
            }

        if(LEVEL == 2):
            plataform_tile_map = {
                "0": self.get_sprite(self.tileset, 1, 40, 16), # tile_DIRT

                "1": self.get_sprite(self.tileset, 0, 39, 16), # tile_WOODS_TOP_LEFT
                "2": self.get_sprite(self.tileset, 1, 39, 16), # tile_WOODS_TOP_CENTER
                "3": self.get_sprite(self.tileset, 2, 39, 16), # tile_WOODS_TOP_RIGHT

                "4": self.get_sprite(self.tileset, 0, 40, 16), # tile_WOODS_MID_LEFT
                "5": self.get_sprite(self.tileset, 2, 40, 16), # tile_WOODS_MID_RIGHT

                "6": self.get_sprite(self.tileset, 0, 41, 16), # tile_WOODS_BOT_LEFT
                "7": self.get_sprite(self.tileset, 1, 41, 16), # tile_WOODS_BOT_CENTER
                "8": self.get_sprite(self.tileset, 2, 41, 16), # tile_WOODS_BOT_RIGHT

                "a": self.get_sprite(self.tileset, 21, 40, 16), # tile_WOODS_CORNER_TOP_LEFT
                "b": self.get_sprite(self.tileset, 20, 40, 16), # tile_WOODS_CORNER_TOP_RIGHT
                "c": self.get_sprite(self.tileset, 21, 39, 16), # tile_WOODS_CORNER_BOT_LEFT
                "d": self.get_sprite(self.tileset, 20, 39, 16), # tile_WOODS_CORNER_BOT_RIGHT

                "e": self.get_sprite(self.tileset, 23, 40, 16), # tile_WOODS_ISLAND_TOP
                "f": self.get_sprite(self.tileset, 3, 40, 16), # tile_WOODS_ISLAND_MID
                "g": self.get_sprite(self.tileset, 3, 41, 16), # tile_WOODS_ISLAND_BOT

                "h": self.get_sprite(self.tileset, 23, 40, 16), # tile_WOODS_STAIRS_AJUST-1
                "i": self.get_sprite(self.tileset, 23, 41, 16), # tile_WOODS_STAIRS_AJUST-2

                "p": self.get_sprite(self.tileset, 28, 2, 16), # tile_BOX-1

                "T": self.get_sprite(self.tileset, 16, 3, 16), # tile_STONE_TOP_LEFT
                "Q": self.get_sprite(self.tileset, 17, 3, 16), # tile_STONE_TOP_CENTER
                "U": self.get_sprite(self.tileset, 18, 3, 16), # tile_STONE_TOP_RIGHT

                "R": self.get_sprite(self.tileset, 16, 4, 16), # tile_STONE_MID_LEFT
                "S": self.get_sprite(self.tileset, 18, 4, 16), # tile_STONE_MID_RIGHT

                "M": self.get_sprite(self.tileset, 21, 43, 16), # tile_STONE_CORNER_TOP_LEFT
                "N": self.get_sprite(self.tileset, 20, 43, 16), # tile_STONE_CORNER_TOP_RIGHT
                "O": self.get_sprite(self.tileset, 21, 42, 16), # tile_STONE_CORNER_BOT_LEFT
                "P": self.get_sprite(self.tileset, 20, 42, 16), # tile_STONE_CORNER_BOT_RIGHT
            
                ":": self._make_decoration_block_auto((21,20), 3, 4), # tile_BLOCK_BOOKSHELF-1
                ";": self._make_decoration_block_auto((25,20), 2, 2), # tile_BLOCK_BOOKSHELF-2
                "/": self._make_decoration_block_auto((25,22), 2, 2), # tile_BLOCK_BOOKSHELF-3
                "^": self._make_decoration_block_auto((24,4), 3, 4), # tile_BLOCK_BOOKSHELF-4
                "~": self._make_decoration_block_auto((28,6), 2, 2), # tile_BLOCK_BOOKSHELF-5

                "|": self._make_decoration_block_auto((31,15), 3, 1), # tile_BLOCK_BED

                "J": self._make_decoration_block_auto((26,16), 3, 1), # tile_BLOCK_TABLE
            }

        # Build platforms if a tile map for platforms was defined for the current level
        if 'plataform_tile_map' in locals():
            for y, row in enumerate(self.map):
                for x, tile_char in enumerate(row):
                    if tile_char in plataform_tile_map:
                        block_surface = plataform_tile_map[tile_char]

                        # Verifica se é o bloco 3x3 (ou outro maior que 1 tile)
                        if tile_char == ":" or tile_char == "^":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 4 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 4 * TILE_SIZE)
                        elif tile_char == ";" or tile_char == "/" or tile_char == "~":
                            img = pygame.transform.scale(block_surface, (2 * TILE_SIZE, 2 * TILE_SIZE))
                            size = pygame.math.Vector2(2 * TILE_SIZE, 2 * TILE_SIZE)
                        elif tile_char == "|" or tile_char == "J":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 1 * TILE_SIZE)
                        else:
                            img = pygame.transform.scale(block_surface, (TILE_SIZE, TILE_SIZE))
                            size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                            
                        position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                        platforms.append(Platform(position, size, img))

        return platforms

    def _load_decorations(self):
        decorations = []

        if(LEVEL == 1):       
            decoration_tile_map = {
                "a": self.get_sprite(self.tileset, 9, 10, 16),  # tile_WEEDS_1
                "b": self.get_sprite(self.tileset, 10, 10, 16),  # tile_WEEDS_2
                "c": self.get_sprite(self.tileset, 11, 10, 16),  # tile_WEEDS_3

                "d": self.get_sprite(self.tileset, 11, 12, 16),  # tile_FLOWERS_1
                "e": self.get_sprite(self.tileset, 11, 13, 16),  # tile_FLOWERS_2
                
                "$": self.get_sprite(self.tileset, 9, 14, 16),

                "(": self.get_sprite(self.tileset, 16, 10, 16),  # tile_BLOCK_LAMP_1
                ")": self.get_sprite(self.tileset, 17, 12, 16),  # tile_BLOCK_LAMP_2

                "f": self._make_decoration_block_auto((9, 11), 3, 1),
                "/": self._make_decoration_block_auto((21, 31), 3, 1),

                "@": self._make_decoration_block_auto((10, 35), 8, 4), # tile_block_WALLS
                "#": self._make_decoration_block_auto((0, 31), 10, 2), # tile_block_ROOF
                "!": self._make_decoration_block_auto((17, 23), 4, 4), # tile_block_POÇO

                "%": self._make_decoration_block_auto((44, 29), 3, 4), # tile_block_TREE-1
                "*": self._make_decoration_block_auto((43, 33), 3, 3), # tile_block_LOG
            }

            for y, row in enumerate(self.map):
                for x, tile_char in enumerate(row):
                    if tile_char in decoration_tile_map:
                        block_surface = decoration_tile_map[tile_char]

                        # Verifica se é o bloco 3x3 (ou outro maior que 1 tile)
                        if tile_char == "@":
                            img = pygame.transform.scale(block_surface, (8 * TILE_SIZE, 4 * TILE_SIZE))
                            size = pygame.math.Vector2(8 * TILE_SIZE, 4 * TILE_SIZE)
                        elif tile_char == "#":
                            img = pygame.transform.scale(block_surface, (10 * TILE_SIZE, 2 * TILE_SIZE))
                            size = pygame.math.Vector2(10 * TILE_SIZE, 2 * TILE_SIZE)
                        elif tile_char == "f":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 1 * TILE_SIZE)
                        elif tile_char == "/":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 1 * TILE_SIZE)
                        elif tile_char == "%":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 4 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 4 * TILE_SIZE)
                        elif tile_char == "*":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 3 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 3 * TILE_SIZE)
                        elif tile_char == "!":
                            img = pygame.transform.scale(block_surface, (4 * TILE_SIZE, 4 * TILE_SIZE))
                            size = pygame.math.Vector2(4 * TILE_SIZE, 4 * TILE_SIZE)
                        else:
                            img = pygame.transform.scale(block_surface, (TILE_SIZE, TILE_SIZE))
                            size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)

                        position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                        decorations.append(Decoration(position, size, img))

        if(LEVEL == 2):       
            decoration_tile_map = {
                "!": self._make_decoration_block_auto((15, 9), 1, 2), # tile_FLOWER-1

                "@": self._make_decoration_block_auto((14, 15), 2, 4), # tile_block_FRAME-1
                "#": self._make_decoration_block_auto((16, 15), 2, 4), # tile_block_FRAME-2
                "-": self._make_decoration_block_auto((25, 1), 2, 2), # tile_block_FRAME-4

                "%": self._make_decoration_block_auto((2, 43), 2, 3), # tile_block_DOOR

                "V": self._make_decoration_block_auto((18, 45), 2, 2), # tile_block_WINDOWS-1
                "W": self._make_decoration_block_auto((20, 45), 2, 2), # tile_block_WINDOWS-2
                "X": self._make_decoration_block_auto((18, 47), 2, 2), # tile_block_WINDOWS-3

                "¨": self._make_decoration_block_auto((32, 14), 2, 1),  # tile_block_BED-DECORATION

                "z": self._make_decoration_block_auto((16, 10), 1, 2),  # tile_block_LAMP
                "<": self.get_sprite(self.tileset, 18, 12, 16),  # tile_LAMP-2

                ")": self.get_sprite(self.tileset, 14, 24, 16),  # tile_UNDERGROUND_PLANT-0
                "*": self.get_sprite(self.tileset, 14, 23, 16),  # tile_UNDERGROUND_PLANT-1
                "&": self.get_sprite(self.tileset, 15, 26, 16),  # tile_UNDERGROUND_PLANT-2
                "(": self.get_sprite(self.tileset, 16, 23, 16),  # tile_UNDERGROUND_PLANT-3

                "j": self.get_sprite(self.tileset, 24, 2, 16),  # tile_HOUSE_PLANT-1
                "k": self.get_sprite(self.tileset, 22, 2, 16),  # tile_HOUSE_PLANT-2
                "l": self.get_sprite(self.tileset, 23, 2, 16),  # tile_HOUSE_PLANT-3

                "x": self.get_sprite(self.tileset, 21, 24, 16),  # tile_POTION-1
                "y": self.get_sprite(self.tileset, 22, 24, 16),  # tile_POTION-2

                "´": self._make_decoration_block_auto((31, 7), 3, 1),  # tile_block_CARPET
                "m": self._make_decoration_block_auto((29, 4), 5, 1),  # tile_block_CARPET-2

                "ç": self._make_decoration_block_auto((21, 1), 1, 2),  # tile_block_SIGN
                
            }

            for y, row in enumerate(self.map):
                for x, tile_char in enumerate(row):
                    if tile_char in decoration_tile_map:
                        block_surface = decoration_tile_map[tile_char]

                        # Verifica se é o bloco 3x3 (ou outro maior que 1 tile)
                        if tile_char == "@" or tile_char == "#" or tile_char == "$":
                            img = pygame.transform.scale(block_surface, (2 * TILE_SIZE, 4 * TILE_SIZE))
                            size = pygame.math.Vector2(2 * TILE_SIZE, 4 * TILE_SIZE)
                        elif tile_char == "%":
                            img = pygame.transform.scale(block_surface, (2 * TILE_SIZE, 3 * TILE_SIZE))
                            size = pygame.math.Vector2(2 * TILE_SIZE, 3 * TILE_SIZE)
                        elif tile_char == "!" or tile_char == "z" or tile_char == "ç":
                            img = pygame.transform.scale(block_surface, (1 * TILE_SIZE, 2 * TILE_SIZE))
                            size = pygame.math.Vector2(1 * TILE_SIZE, 2 * TILE_SIZE)
                        elif tile_char == "-" or tile_char == "V" or tile_char == "W" or tile_char == "X":
                            img = pygame.transform.scale(block_surface, (2 * TILE_SIZE, 2 * TILE_SIZE))
                            size = pygame.math.Vector2(2 * TILE_SIZE, 2 * TILE_SIZE)
                        elif tile_char == "¨":
                            img = pygame.transform.scale(block_surface, (2 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(2 * TILE_SIZE, 1 * TILE_SIZE)
                        elif tile_char == "´":
                            img = pygame.transform.scale(block_surface, (3 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(3 * TILE_SIZE, 1 * TILE_SIZE)
                        elif tile_char == "m":
                            img = pygame.transform.scale(block_surface, (5 * TILE_SIZE, 1 * TILE_SIZE))
                            size = pygame.math.Vector2(5 * TILE_SIZE, 1 * TILE_SIZE)
                        else:
                            img = pygame.transform.scale(block_surface, (TILE_SIZE, TILE_SIZE))
                            size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)

                        position = pygame.math.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                        decorations.append(Decoration(position, size, img))

        return decorations


    def _make_decoration_block_auto(self, start_tile, block_width, block_height, tile_size=16):
        block_surface = pygame.Surface((block_width * tile_size, block_height * tile_size), pygame.SRCALPHA)

        start_x, start_y = start_tile
        for row in range(block_height):
            for col in range(block_width):
                tx = start_x + col
                ty = start_y + row
                img = self.get_sprite(self.tileset, tx, ty, tile_size)  # usa 16 aqui
                block_surface.blit(img, (col * tile_size, row * tile_size))

        return block_surface

    def _load_doors(self):
        from door import Door
        doors = []

        # Sprites para porta fechada
        door_closed_map = {
            "D": self.get_sprite(self.tileset, 2, 45, 16), #tile_DOOR_BOT_L_CLOSED
            "E": self.get_sprite(self.tileset, 3, 45, 16), #tile_DOOR_BOT_R_CLOSED
            "F": self.get_sprite(self.tileset, 2, 44, 16), #tile_DOOR_MID_L_CLOSED
            "G": self.get_sprite(self.tileset, 3, 44, 16), #tile_DOOR_MID_R_CLOSED
            "H": self.get_sprite(self.tileset, 2, 43, 16), #tile_DOOR_TOP_L_CLOSED
            "I": self.get_sprite(self.tileset, 3, 43, 16), #tile_DOOR_TOP_R_CLOSED
        }

        # Sprites para porta aberta (usando coordenadas diferentes no tileset)
        door_open_map = {
            "D": self.get_sprite(self.tileset, 0, 45, 16), #tile_DOOR_BOT_L_OPEN
            "E": self.get_sprite(self.tileset, 1, 45, 16), #tile_DOOR_BOT_R_OPEN
            "F": self.get_sprite(self.tileset, 0, 44, 16), #tile_DOOR_MID_L_OPEN
            "G": self.get_sprite(self.tileset, 1, 44, 16), #tile_DOOR_MID_R_OPEN
            "H": self.get_sprite(self.tileset, 0, 43, 16), #tile_DOOR_TOP_L_OPEN
            "I": self.get_sprite(self.tileset, 1, 43, 16), #tile_DOOR_TOP_R_OPEN
        }

        for y, row in enumerate(self.map):
            for x, tile_char in enumerate(row):
                if tile_char in door_closed_map:
                    closed_img = pygame.transform.scale(
                        door_closed_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    open_img = pygame.transform.scale(
                        door_open_map[tile_char], (TILE_SIZE, TILE_SIZE))
                    position = pygame.math.Vector2(
                        x * TILE_SIZE, y * TILE_SIZE)
                    size = pygame.math.Vector2(TILE_SIZE, TILE_SIZE)
                    door = Door(position, size, closed_img, open_img)
                    doors.append(door)

        return doors

    def load_player_sprites(self):

        base_path = os.path.dirname(__file__)
        sprite_size = (32, 48)
        sprite_size_die = (16, 16)

        idle_path = os.path.join(
            base_path, '..', 'resources', 'idle', 'Player_Idle.gif')
        idle_gif = AnimatedGif(idle_path, sprite_size)
        run_path = os.path.join(
            base_path, '..', 'resources', 'run', 'Player_Run.gif')
        run_gif = AnimatedGif(run_path, sprite_size)
        run_left_gif = run_gif.get_flipped_frames()

        die_path = os.path.join(
            base_path, '..', 'resources', 'die', 'Player_Die.gif')
        die_gif = AnimatedGif(die_path, sprite_size_die)

        return {
            'idle': idle_gif,
            'idle_left': idle_gif,
            'run_right': run_gif,
            'run_left': run_left_gif,
            'die': die_gif
        }

    def load_player_sprites2(self):

        base_path = os.path.dirname(__file__)
        sprite_size = (32, 48)
        sprite_size_die = (20, 20)

        idle_path = os.path.join(
            base_path, '..', 'resources', 'idle', 'Player_Idle_b.gif')
        idle_gif = AnimatedGif(idle_path, sprite_size)
        run_path = os.path.join(
            base_path, '..', 'resources', 'run', 'Player_Run_b.gif')
        run_gif = AnimatedGif(run_path, sprite_size)
        run_left_gif = run_gif.get_flipped_frames()

        die_path = os.path.join(
            base_path, '..', 'resources', 'die', 'Player_Die.gif')
        die_gif = AnimatedGif(die_path, sprite_size_die)

        return {
            'idle': idle_gif,
            'idle_left': idle_gif,
            'run_right': run_gif,
            'run_left': run_left_gif,
            'die': die_gif
        }

    def _load_door_sound(self):
        """Carrega o som para quando a porta é ativada"""
        try:
            base_path = os.path.dirname(__file__)
            sound_path = os.path.join(base_path, '..', 'resources', 'sounds', 'key.wav')
            self.door_sound = pygame.mixer.Sound(sound_path)
            self.door_sound.set_volume(0.7)
        except:
            self.door_sound = None

    def _load_moving_block_sound(self):
        """Carrega o som para quando um bloco/controlado se move (ativação de botão)"""
        try:
            base_path = os.path.dirname(__file__)
            sound_path = os.path.join(base_path, '..', 'resources', 'sounds', 'moving_block.mp3')
            self.moving_block_sound = pygame.mixer.Sound(sound_path)
            self.moving_block_sound.set_volume(0.7)
        except:
            # Tentar alternativa .wav caso mp3 não seja aceito pelo mixer
            try:
                sound_path = os.path.join(base_path, '..', 'resources', 'sounds', 'moving_block.wav')
                self.moving_block_sound = pygame.mixer.Sound(sound_path)
                self.moving_block_sound.set_volume(0.7)
            except:
                self.moving_block_sound = None

    def _load_background_music(self):
        base_path = os.path.dirname(__file__)

        if(LEVEL == 1): 
            music_path = os.path.join(
                base_path, '..', 'resources', 'sounds', 'background_sound_1.mp3')
        
        if(LEVEL == 2): 
            music_path = os.path.join(
                base_path, '..', 'resources', 'sounds', 'background_sound_2.mp3')

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def _create_fallback_sprites(self, sprite_size):

        simple_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
        simple_surface.fill((0, 255, 0))

        fake_gif = AnimatedGif.__new__(AnimatedGif)
        fake_gif.m_frames = [simple_surface]
        fake_gif.m_frame_count = 1
        fake_gif.m_current_frame = 0
        fake_gif.m_frame_timer = 0
        fake_gif.m_animation_speed = 5

        return {
            'idle': fake_gif,
            'idle_left': fake_gif,
            'run_right': fake_gif,
            'run_left': fake_gif
        }

    # === MÉTODOS DE GERENCIAMENTO DE ÁREAS SECRETAS ===
    
    def add_secret_area(self, x, y, width, height, color_hex):

        secret_area = SecretArea(x, y, width, height, color_hex)
        self.secret_areas.append(secret_area)
        print(f"Nova área secreta adicionada em ({x}, {y}) com tamanho {width}x{height}")
        return secret_area
    
    def remove_secret_area(self, index):

        if 0 <= index < len(self.secret_areas):
            removed_area = self.secret_areas.pop(index)
            print(f"Área secreta removida: {removed_area.get_info()}")
            return True
        return False
    
    def remove_secret_area_at_position(self, x, y):

        removed_count = 0
        self.secret_areas = [area for area in self.secret_areas 
                           if not area.rect.collidepoint(x, y)]
        
        if removed_count > 0:
            print(f"Removidas {removed_count} áreas secretas na posição ({x}, {y})")
        
        return removed_count
    
    def get_secret_areas_info(self):

        return [area.get_info() for area in self.secret_areas]
    
    def clear_all_secret_areas(self):
        
        count = len(self.secret_areas)
        self.secret_areas.clear()
        print(f"Todas as {count} áreas secretas foram removidas")

    # === MÉTODOS DE GERENCIAMENTO DE PLACAS DE PRESSÃO ===
    
    def add_pressure_plate(self, x, y, plate_id, sprite_inactive, sprite_active):

        plate = PressurePlate(
            position=pygame.math.Vector2(x, y),
            size=pygame.math.Vector2(TILE_SIZE, TILE_SIZE),
            plate_id=plate_id,
            sprite_inactive=sprite_inactive,
            sprite_active=sprite_active
        )
        self.pressure_plates.append(plate)
        print(f"Placa de pressão '{plate_id}' adicionada em ({x}, {y})")
        return plate
    
    def add_controlled_block(self, x, y, plate_id, block_type, sprite_normal, sprite_disabled=None):

        block = ControlledBlock(
            position=pygame.math.Vector2(x, y),
            size=pygame.math.Vector2(TILE_SIZE, TILE_SIZE),
            pressure_plate_id=plate_id,
            block_type=block_type,
            sprite_normal=sprite_normal,
            sprite_disabled=sprite_disabled
        )
        self.controlled_blocks.append(block)
        print(f"Bloco controlado adicionado em ({x}, {y}) para placa '{plate_id}'")
        return block
    
    def get_pressure_plate_info(self):
        """Retorna informações de debug das placas de pressão"""
        return [plate.get_info() for plate in self.pressure_plates]
    
    def get_controlled_blocks_info(self):
        """Retorna informações de debug dos blocos controlados"""
        return [block.get_info() for block in self.controlled_blocks]
