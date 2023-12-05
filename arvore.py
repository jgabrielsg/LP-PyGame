import pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group, image_path=None):
        super().__init__(group)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)