import pygame as pg
from PIL import Image
import os

class AnimatedGif:
    def __init__(self, gif_path, scale_size=None):

        self.m_frames = []
        self.m_frame_durations = []  # Store duration for each frame
        self.m_current_frame = 0
        self.m_frame_count = 0
        self.m_frame_timer = 0
        self.m_current_frame_duration = 100  # Default duration in milliseconds


        gif = Image.open(gif_path)
            

        frame_index = 0
        while frame_index < gif.n_frames:
            gif.seek(frame_index)
            frame = gif.copy()

            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')

            if scale_size:
                frame = frame.resize(scale_size, Image.Resampling.NEAREST)

            frame_data = frame.tobytes()
            pygame_frame = pg.image.frombytes(frame_data, frame.size, 'RGBA')
            
            # Get frame duration from GIF (in milliseconds)
            duration = gif.info.get('duration', 100)  # Default to 100ms if not specified
            
            self.m_frames.append(pygame_frame)
            self.m_frame_durations.append(duration)
            frame_index += 1
            
        self.m_frame_count = len(self.m_frames)
        if self.m_frame_count > 0:
            self.m_current_frame_duration = self.m_frame_durations[0]
    
    def get_current_frame(self):
        if self.m_frame_count == 0:
            return None
        return self.m_frames[self.m_current_frame]
    
    def update(self, delta_time_ms=16.67):  # Default ~60 FPS
        if self.m_frame_count <= 1:
            return
        
        self.m_frame_timer += delta_time_ms
        if self.m_frame_timer >= self.m_current_frame_duration:
            self.m_frame_timer = 0
            self.m_current_frame = (self.m_current_frame + 1) % self.m_frame_count
            # Update duration for the new current frame
            self.m_current_frame_duration = self.m_frame_durations[self.m_current_frame]
    
    def reset(self):

        self.m_current_frame = 0
        self.m_frame_timer = 0
    
    def get_flipped_frames(self):

        flipped_frames = []
        for frame in self.m_frames:
            flipped_frame = pg.transform.flip(frame, True, False)
            flipped_frames.append(flipped_frame)
        

        flipped_gif = AnimatedGif.__new__(AnimatedGif)
        flipped_gif.m_frames = flipped_frames
        flipped_gif.m_frame_durations = self.m_frame_durations.copy()  # Copy frame durations
        flipped_gif.m_frame_count = len(flipped_frames)
        flipped_gif.m_current_frame = 0
        flipped_gif.m_frame_timer = 0
        flipped_gif.m_current_frame_duration = flipped_gif.m_frame_durations[0] if flipped_gif.m_frame_durations else 100
        
        return flipped_gif
