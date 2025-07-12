from object import ObjectDynamic
from collider import Collider

import pygame as pg
from object import ObjectDynamic  
from enum import Enum
import os

class Button(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2

class Player(ObjectDynamic):
    def __init__(self, position, sprites, velocity, size, my_keys):
        super().__init__(position, size, velocity)
        self.sprites = sprites
        self.m_score = 0
        self.m_lives = 3
        self.animation = 0
        self.animation_frame = 0
        self.last_animation = 0
        self.m_move_to_right = False
        self.m_move_to_left = False
        self.m_is_on_ground = False
        self.m_my_keys = my_keys  
        self.gravity = 50.8
        
        # Inicializar mixer de áudio
        pg.mixer.init()
        
        # Carregar sons
        self._load_sounds()
    
    

    def render(self, surface):
        anims = self.sprites[self.animation]
        index = self.animation_frame // 7 % len(anims)
        surface.blit(anims[index], self._position)
        self.animation_frame = (self.animation_frame + 1) % (len(anims) * 7)

    def update(self, delta_time):
        velocity = self.get_velocity()
        position = self._position

        velocity.y += self.gravity * delta_time
        position += velocity * delta_time

        self.set_velocity(velocity)
        self.set_position(position)

    def collect_points(self, points):
        self.m_score += points
        print(f"Pontos coletados: +{points}! Score total: {self.m_score}")
        
        # Tocar som de coleta
        if self.collect_sound:
            self.collect_sound.play()
    
    def get_score(self):
        return self.m_score
    
    def verify_keyboard(self):
        teclas = pg.key.get_pressed()
        current_velocity = self.get_velocity()

        if teclas[self.m_my_keys[Button.LEFT.value]]:
                self.m_move_to_left = True
                print("LEFT pressed")
                self.animation = 3
                self.set_velocity(pg.math.Vector2(-40.0, current_velocity.y))
        elif teclas[self.m_my_keys[Button.RIGHT.value]]:
                self.m_move_to_right = True
                print("RIGHT pressed")
                self.animation = 2
                self.set_velocity(pg.math.Vector2(40.0, current_velocity.y))
        else:
                # Para o movimento horizontal quando nenhuma tecla de direção está pressionada
                self.m_move_to_left = False
                self.m_move_to_right = False
                self.animation = 2  # Volta para animação idle
                self.set_velocity(pg.math.Vector2(0.0, current_velocity.y))

        if teclas[self.m_my_keys[Button.UP.value]]:
            if self.m_is_on_ground:
                self.set_velocity(pg.math.Vector2(current_velocity.x, -130.0))
                print("Jumping UP")
                
                # Tocar som de pulo
                if self.jump_sound:
                    self.jump_sound.play()
        print('Is on ground:', self.m_is_on_ground)
    
    def _load_sounds(self):
        """Carrega os arquivos de som do jogador"""
        try:
            base_path = os.path.dirname(__file__)
            sounds_path = os.path.join(base_path, '..', 'resources', 'sounds')
            
            # Tentar carregar sons (se não existirem, usar None)
            try:
                self.jump_sound = pg.mixer.Sound(os.path.join(sounds_path, 'jump.wav'))
                self.jump_sound.set_volume(0.5)
            except:
                self.jump_sound = None
                print("Som de pulo não encontrado - continuando sem som")
            
            try:
                self.collect_sound = pg.mixer.Sound(os.path.join(sounds_path, 'collect.wav'))
                self.collect_sound.set_volume(0.7)
            except:
                self.collect_sound = None
                print("Som de coleta não encontrado - continuando sem som")
                
            try:
                self.walk_sound = pg.mixer.Sound(os.path.join(sounds_path, 'walk.wav'))
                self.walk_sound.set_volume(0.3)
            except:
                self.walk_sound = None
                print("Som de caminhada não encontrado - continuando sem som")
                
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
            self.jump_sound = None
            self.collect_sound = None
            self.walk_sound = None