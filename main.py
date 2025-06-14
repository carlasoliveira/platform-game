import pygame as pg
from player import Player

# Inicialização
pg.init()
screen = pg.display.set_mode((1280, 768))
clock = pg.time.Clock()
def load_player_sprites():
    idle = [pg.transform.scale(pg.image.load('C:/Users/cardo/Desktop/platform-game/resources/idle/1.PNG'), (128, 80))]
    right = [pg.transform.scale(pg.image.load(f'C:/Users/cardo/Desktop/platform-game/resources/run/{i}.PNG'), (128, 80)) for i in range(1, 4)]
    left = [pg.transform.flip(img, True, False) for img in right]
    idle_left = [pg.transform.flip(img, True, False) for img in idle]
    return [idle, idle_left, right, left]

sprites = load_player_sprites()
position = [300, 600]  # Posição inicial do jogador
size = [46, 54]        # Tamanho da caixa de colisão
velocity = [0, 0]      # Velocidade inicial (x, y)

# Criando jogador
player = Player(sprites, position, size, velocity)

# Mapa simples (para colisão)
game_map = [[' ']*20 for _ in range(11)] + [['2']*20]  # Chão na última linha

# Loop principal
running = True
while running:
    screen.fill((135, 206, 250))  # Céu azul de fundo
    delta_time = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player.jump()

    keys = pg.key.get_pressed()
    player.move(keys, game_map)
    player.update(delta_time, game_map)
    player.render(screen)

    pg.display.flip()

pg.quit()
