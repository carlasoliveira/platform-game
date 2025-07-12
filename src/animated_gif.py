import pygame as pg
from PIL import Image
import os

class AnimatedGif:
    def __init__(self, gif_path, scale_size=None):

        self.frames = []
        self.current_frame = 0
        self.frame_count = 0
        self.animation_speed = 5 
        self.frame_timer = 0


        gif = Image.open(gif_path)
            

        frame_index = 0
        while True:
                try:
                    gif.seek(frame_index)
                    frame = gif.copy()

                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')

                    if scale_size:
                        frame = frame.resize(scale_size, Image.Resampling.NEAREST)

                    frame_data = frame.tobytes()
                    pygame_frame = pg.image.frombytes(frame_data, frame.size, 'RGBA')
                    
                    self.frames.append(pygame_frame)
                    frame_index += 1
                    
                except EOFError:

                    break
            
        self.frame_count = len(self.frames)
          
            
        # except Exception as e:
        #    
        #     # Criar frame vazio como fallback
        #     if scale_size:
        #         empty_frame = pg.Surface(scale_size, pg.SRCALPHA)
        #     else:
        #         empty_frame = pg.Surface((32, 32), pg.SRCALPHA)
        #     empty_frame.fill((255, 0, 255, 128))  # Rosa transparente
        #     self.frames = [empty_frame]
        #     self.frame_count = 1
    
    def get_current_frame(self):
        if self.frame_count == 0:
            return None
        return self.frames[self.current_frame]
    
    def update(self):
        if self.frame_count <= 1:
            return
        
        self.frame_timer += 1
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
    
    def reset(self):

        self.current_frame = 0
        self.frame_timer = 0
    
    def get_flipped_frames(self):

        flipped_frames = []
        for frame in self.frames:
            flipped_frame = pg.transform.flip(frame, True, False)
            flipped_frames.append(flipped_frame)
        

        flipped_gif = AnimatedGif.__new__(AnimatedGif)
        flipped_gif.frames = flipped_frames
        flipped_gif.frame_count = len(flipped_frames)
        flipped_gif.current_frame = 0
        flipped_gif.frame_timer = 0
        flipped_gif.animation_speed = self.animation_speed
        
        return flipped_gif
