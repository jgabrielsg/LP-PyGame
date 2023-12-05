import pygame
import random

class Music:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    @property
    def background(self):
        song_path = "assets/sounds/background.mp3" 
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

    @property
    def shot(self):
        song_path = ""
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

    @property
    def got_damage(self):
        song_path = ""
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

    def stop_song(self):
        pygame.mixer.music.stop()
