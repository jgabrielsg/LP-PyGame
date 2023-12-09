import pygame
import random

class Music:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    @property
    def background(self):
        sound_path = "assets/sounds/background.mp3" 
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    @property
    def shot(self):
        sound_path = "assets/sounds/tiro.mp3"
        damage_sound = pygame.mixer.Sound(sound_path)
        damage_sound.play()

    @property
    def damage(self):
        sound_path = ""
        damage_sound = pygame.mixer.Sound(sound_path)
        damage_sound.play()

    def stop_song(self):
        pygame.mixer.music.stop()
