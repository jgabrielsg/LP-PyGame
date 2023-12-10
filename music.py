import pygame
import random

class Music:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.volume = 1

    @property
    def background(self):
        sound_path = "assets/sounds/background.mp3" 
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    @property
    def shot(self):
        sound_path = "assets/sounds/tiro.mp3"
        shot_sound = pygame.mixer.Sound(sound_path)
        shot_sound.set_volume(self.volume)
        shot_sound.play()

    @property
    def damage(self):
        sound_path = ""
        damage_sound = pygame.mixer.Sound(sound_path)
        damage_sound.set_volume(self.volume)
        damage_sound.play()

    @property
    def mana(self):
        sound_path = "assets/sounds/mana.mp3"
        mana_sound = pygame.mixer.Sound(sound_path)
        mana_sound.set_volume(self.volume)
        mana_sound.play()

    def stop_song(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = volume/100
